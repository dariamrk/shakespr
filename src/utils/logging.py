# src/utils/logging.py
import logging
import os
import sentry_sdk
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent.parent / 'data' / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'bot.log'),
        logging.StreamHandler()
    ]
)

# Create logger
logger = logging.getLogger('shakespr')

def setup_logging():
    """Initialize logging configuration"""
    # Initialize Sentry if DSN is provided
    sentry_dsn = os.getenv('SENTRY_DSN')
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=1.0,
            environment=os.getenv('ENVIRONMENT', 'development')
        )
    
    return logger

# Export logger for use in other modules
__all__ = ['logger', 'setup_logging']
