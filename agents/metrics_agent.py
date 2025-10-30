# agents/metrics_agent.py
import json
import os
import time
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

METRICS_PATH = os.path.join("data", "metrics", "performance.json")


class MetricsAgent:
    """
    Tracks and stores runtime metrics such as latency, success/failure rate, and timestamps.
    """

    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
            "last_updated": None
        }
        self._load_existing_metrics()

    def _load_existing_metrics(self):
        """Load existing metrics from JSON if available."""
        if os.path.exists(METRICS_PATH):
            try:
                with open(METRICS_PATH, "r") as f:
                    self.metrics = json.load(f)
                logger.info("Loaded existing metrics data.")
            except Exception as e:
                logger.warning(f"Failed to load metrics file: {e}")

    def _save_metrics(self):
        """Write metrics to JSON file."""
        os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
        with open(METRICS_PATH, "w") as f:
            json.dump(self.metrics, f, indent=4)
        logger.debug("Metrics saved successfully.")

    def track(self, success: bool, duration: float):
        """Record a single request’s outcome."""
        self.metrics["total_requests"] += 1
        if success:
            self.metrics["successful_requests"] += 1
        else:
            self.metrics["failed_requests"] += 1

        # Update average response time (rolling)
        total = self.metrics["average_response_time"] * (self.metrics["total_requests"] - 1)
        self.metrics["average_response_time"] = (total + duration) / self.metrics["total_requests"]
        self.metrics["last_updated"] = datetime.utcnow().isoformat()

        self._save_metrics()

    def measure(self, func):
        """Decorator to measure function performance."""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                self.track(success=True, duration=duration)
                logger.info(f"{func.__name__} executed successfully in {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                self.track(success=False, duration=duration)
                logger.error(f"{func.__name__} failed after {duration:.2f}s: {e}")
                raise e
        return wrapper
