from pathlib import Path
css = '''/* SOC Alert Dashboard Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --bg-primary: #f8fafc;
  --bg-secondary: #ffffff;
  --bg-card: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --accent: #2563eb;
  --accent-soft: #bfdbfe;
  --success: #16a34a;
  --border: #e2e8f0;
  --shadow: rgba(15, 23, 42, 0.08);
}

body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  min-height: 100vh;
}

.dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: var(--bg-secondary);
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--accent);
}

.trigger-btn {
  background: var(--success);
  color: white;
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 999px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.trigger-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 12px 24px rgba(22, 163, 74, 0.18);
}

.trigger-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.status {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.95rem;
  color: var(--text-secondary);
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: 0 0 10px rgba(22, 163, 74, 0.35);
}

.last-update {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 1rem;
  color: var(--text-secondary);
}

.empty-state h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
}

.alerts-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.alert-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 10px 30px var(--shadow);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.alert-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 36px rgba(15, 23, 42, 0.12);
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid var(--border);
}

.alert-time {
  font-size: 0.95rem;
  color: var(--text-secondary);
}

.threat-badge {
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: white;
}

.alert-body {
  padding: 1.5rem;
}

.alert-section {
  margin-bottom: 1.5rem;
}

.alert-section:last-child {
  margin-bottom: 0;
}

.alert-section h3 {
  font-size: 0.8rem;
  color: var(--accent);
  margin-bottom: 0.5rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.alert-type,
.analysis-item,
.log-item {
  font-size: 0.95rem;
  color: var(--text-primary);
  line-height: 1.6;
}

.alert-type {
  padding: 1rem;
  border-radius: 12px;
  background: var(--accent-soft);
  border: 1px solid rgba(37, 99, 235, 0.15);
  color: var(--accent);
  font-weight: 700;
}

.logs-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.log-item {
  padding: 0.9rem 1rem;
  border-radius: 12px;
  background: #f1f5f9;
  border: 1px solid #dbeafe;
  color: var(--text-secondary);
  font-family: 'Segoe UI', system-ui, sans-serif;
}

.analysis-section {
  background: #f8fafc;
  border: 1px solid #dbeafe;
  border-radius: 14px;
  padding: 1.25rem;
}

.analysis-item {
  margin-bottom: 0.85rem;
}

.analysis-item:last-child {
  margin-bottom: 0;
}

.analysis-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.analysis-list-item,
.analysis-item pre {
  padding: 0.9rem;
  border-radius: 12px;
  background: #eef2ff;
  border: 1px solid #dbeafe;
  overflow-x: auto;
  color: var(--text-primary);
  font-family: 'Segoe UI', system-ui, sans-serif;
}

footer.footer {
  display: none;
}

@media (max-width: 768px) {
  .header,
  .main-content {
    padding: 1rem;
  }

  .alert-header,
  .alert-body {
    padding: 1rem;
  }

  .trigger-btn {
    width: 100%;
  }
}
'''
Path(r'c:/Users/saone/Desktop/splunk_Pipleine/frontend/src/App.css').write_text(css, encoding='utf-8')
print('written')
'''
