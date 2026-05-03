import LogsBlock from './LogsBlock'
import AnalysisBlock from './AnalysisBlock'
import { parseAnalysis, getLogs, getThreatColor } from './helpers'

function formatRelativeTime(timestamp) {
  const diffMs = Date.now() - timestamp * 1000
  if (diffMs < 0) return 'just now'

  const seconds = Math.floor(diffMs / 1000)
  if (seconds < 60) return `${seconds} sec${seconds === 1 ? '' : 's'} ago`

  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `${minutes} min${minutes === 1 ? '' : 's'} ago`

  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} hour${hours === 1 ? '' : 's'} ago`

  const days = Math.floor(hours / 24)
  return `${days} day${days === 1 ? '' : 's'} ago`
}

function AlertCard({ alert }) {
  const parsed = parseAnalysis(alert.analysis)
  const logs = getLogs(alert)
  const relativeTime = formatRelativeTime(alert.timestamp)

  return (
    <div className="alert-card">
      <div className="alert-header">
        <span className="alert-time">
          {new Date(alert.timestamp * 1000).toLocaleString()} · {relativeTime}
        </span>
        <span
          className="threat-badge"
          style={{ backgroundColor: getThreatColor(parsed?.threat_level) }}
        >
          {parsed?.threat_level || 'UNKNOWN'}
        </span>
      </div>

      <div className="alert-body">
        <div className="alert-section">
          <h3>ALERT TYPE</h3>
          <p className="alert-type">
            {parsed?.attack_type || alert.type || 'Unknown alert type'}
          </p>
        </div>

        <LogsBlock logs={logs} />
        <AnalysisBlock analysis={parsed} />
      </div>
    </div>
  )
}

export default AlertCard
