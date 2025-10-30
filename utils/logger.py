# utils/logger.py
import logging
from datetime import datetime
import os

# Ensure folder exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=f"logs/holidayplanner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)
