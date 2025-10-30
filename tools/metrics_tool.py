# tools/metrics_tool.py
import json, os
from datetime import datetime

class MetricsTracker:
    def __init__(self):
        self.events = []
        os.makedirs("data/metrics", exist_ok=True)

    def log_event(self, name: str, details: dict = None):
        entry = {
            "time": datetime.now().isoformat(),
            "event": name,
            "details": details or {}
        }
        self.events.append(entry)

    def save_metrics(self):
        filename = f"data/metrics/metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=4, ensure_ascii=False)
        print(f"✅ Metrics saved to {filename}")
