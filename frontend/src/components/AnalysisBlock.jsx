function renderAnalysisValue(value) {
  if (value === null || value === undefined) return 'N/A'
  if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
    return value
  }

  if (Array.isArray(value)) {
    return (
      <div className="analysis-list">
        {value.map((item, index) => (
          <div key={index} className="analysis-list-item">
            {typeof item === 'object' ? JSON.stringify(item, null, 2) : item}
          </div>
        ))}
      </div>
    )
  }

  if (typeof value === 'object') {
    return <pre>{JSON.stringify(value, null, 2)}</pre>
  }

  return String(value)
}

function AnalysisBlock({ analysis }) {
  if (!analysis) return null

  return (
    <div className="alert-section analysis-section">
      <h3>AI ANALYSIS</h3>
      <div className="analysis-item">
        <b>Summary:</b> {renderAnalysisValue(analysis.summary)}
      </div>
      <div className="analysis-item">
        <b>Attack Type:</b> {renderAnalysisValue(analysis.attack_type)}
      </div>
      <div className="analysis-item">
        <b>Recommended Action:</b> {renderAnalysisValue(analysis.recommended_action)}
      </div>
    </div>
  )
}

export default AnalysisBlock
