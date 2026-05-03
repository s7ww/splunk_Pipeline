export const parseAnalysis = (analysis) => {
  if (!analysis) return null
  if (typeof analysis === 'object') return analysis

  try {
    let clean = analysis.trim()

    if (clean.includes('```')) {
      clean = clean.split('```')[1]
      clean = clean.replace('json', '').trim()
    }

    const jsonStart = clean.indexOf('{')
    const jsonEnd = clean.lastIndexOf('}')
    if (jsonStart !== -1 && jsonEnd !== -1) {
      clean = clean.substring(jsonStart, jsonEnd + 1)
    }

    return JSON.parse(clean)
  } catch {
    return {
      summary: analysis,
      attack_type: 'Unknown',
      recommended_action: 'Check raw output',
      threat_level: 'unknown'
    }
  }
}

export const getLogs = (alert) => {
  return alert.related_logs || alert.logs || []
}

export const getThreatColor = (level) => {
  const colors = {
    critical: '#ef4444',
    high: '#f97316',
    medium: '#eab308',
    low: '#22c55e'
  }
  return colors[level?.toLowerCase()] || '#6b7280'
}
