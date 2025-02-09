# src/utils/database.py
import os
import psycopg2
from contextlib import contextmanager
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logger = logging.getLogger(__name__)

# Load environment variables
env_path = Path(__file__).parent.parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

# Database configurations
NUMBEO_DB_CONFIG = {
    'dbname': os.getenv('NUMBEO_DB_NAME'),
    'user': os.getenv('NUMBEO_DB_USER'),
    'password': os.getenv('NUMBEO_DB_PASSWORD'),
    'host': os.getenv('NUMBEO_DB_HOST'),
    'port': os.getenv('NUMBEO_DB_PORT')
}

USER_DB_CONFIG = {
    'dbname': os.getenv('USER_DB_NAME'),
    'user': os.getenv('USER_DB_USER'),
    'password': os.getenv('USER_DB_PASSWORD'),
    'host': os.getenv('USER_DB_HOST'),
    'port': os.getenv('USER_DB_PORT')
}

def test_config():
    """Print current configuration for debugging"""
    print("Numbeo DB Config:", NUMBEO_DB_CONFIG)
    print("User DB Config:", USER_DB_CONFIG)

@contextmanager
def get_numbeo_db_connection():
    """Context manager for Numbeo database connection"""
    conn = None
    try:
        conn = psycopg2.connect(**NUMBEO_DB_CONFIG)
        yield conn
    except Exception as e:
        logger.error(f"Error connecting to Numbeo database: {e}")
        raise
    finally:
        if conn is not None:
            conn.close()

@contextmanager
def get_user_db_connection():
    """Context manager for user database connection"""
    conn = None
    try:
        conn = psycopg2.connect(**USER_DB_CONFIG)
        yield conn
    except Exception as e:
        logger.error(f"Error connecting to user database: {e}")
        raise
    finally:
        if conn is not None:
            conn.close()

def init_user_db():
    """Initialize user database schema"""
    try:
        with get_user_db_connection() as conn:
            with conn.cursor() as cur:
                # Read and execute schema file
                schema_path = os.path.join(
                    os.path.dirname(__file__),
                    '../../sql/user_data/schema/init.sql'
                )
                with open(schema_path, 'r') as f:
                    cur.execute(f.read())
                conn.commit()
                logger.info("User database schema initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing user database: {e}")
        raise
