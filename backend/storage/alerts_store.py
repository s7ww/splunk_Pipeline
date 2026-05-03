import json
from pathlib import Path

STORAGE_DIR = Path(__file__).resolve().parent
ALERTS_FILE = STORAGE_DIR / 'alerts.json'
MAX_ALERTS = 200

ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_alerts():
    if not ALERTS_FILE.exists():
        return []

    try:
        with ALERTS_FILE.open('r', encoding='utf-8') as f:
            alerts = json.load(f)
            if not isinstance(alerts, list):
                return []
            return sorted(alerts, key=lambda item: item.get('timestamp', 0), reverse=True)
    except Exception:
        return []


def save_alerts(alerts):
    try:
        with ALERTS_FILE.open('w', encoding='utf-8') as f:
            json.dump(alerts, f, indent=2)
    except Exception as e:
        print('Unable to save alerts:', e)


def add_alert(alert):
    alerts = load_alerts()
    alerts.insert(0, alert)
    alerts = alerts[:MAX_ALERTS]
    save_alerts(alerts)
    return alerts
