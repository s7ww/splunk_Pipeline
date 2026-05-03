import { useState, useEffect } from 'react'
import './App.css'
import AlertCard from './components/AlertCard'

function App() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(null)
  const [triggering, setTriggering] = useState(false)

  const triggerAlert = async () => {
    setTriggering(true)
    try {
      await fetch('http://localhost:9000/trigger-alert', {
        method: 'POST'
      })

      const res = await fetch('http://localhost:9000/alerts')
      const data = await res.json()

      if (data.alerts) {
        setAlerts(data.alerts)
        setLastUpdate(new Date())
      }
    } catch (error) {
      console.error('Trigger failed:', error)
    }
    setTriggering(false)
  }

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await fetch('http://localhost:9000/alerts')
        const data = await res.json()

        if (data.alerts) {
          setAlerts(data.alerts)
          setLastUpdate(new Date())
        }
      } catch {
        // backend not ready
      }
      setLoading(false)
    }

    fetchAlerts()
    const interval = setInterval(fetchAlerts, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="dashboard">
      <header className="header">
        <h1>SOC Alert Monitor</h1>

        <div className="status">
          <span>{loading ? 'Connecting...' : 'Live'}</span>
          {lastUpdate && <span>Last update: {lastUpdate.toLocaleTimeString()}</span>}
        </div>

        <button onClick={triggerAlert} disabled={triggering}>
          {triggering ? 'Triggering...' : 'Trigger Alert'}
        </button>
      </header>

      <main className="main-content">
        {alerts.length === 0 ? (
          <p>No alerts yet</p>
        ) : (
          alerts.map((alert, i) => <AlertCard key={i} alert={alert} />)
        )}
      </main>
    </div>
  )
}

export default App
