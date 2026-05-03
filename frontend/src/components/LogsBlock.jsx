function LogsBlock({ logs }) {
  if (!logs || logs.length === 0) return null

  return (
    <div className="alert-section">
      <h3>RELATED LOGS</h3>
      <div className="logs-list">
        {logs.map((log, i) => (
          <div key={i} className="log-item">
            {log}
          </div>
        ))}
      </div>
    </div>
  )
}

export default LogsBlock
