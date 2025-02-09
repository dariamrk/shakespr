# src/data/users/crud.py
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any
import logging
from ...utils.database import get_user_db_connection

logger = logging.getLogger(__name__)

async def get_user_profile(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user profile from database"""
    try:
        with get_user_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM bot.user_profiles 
                    WHERE user_id = %s
                """, (user_id,))
                return cur.fetchone()
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        return None

async def update_user_profile(
    user_id: int,
    first_name: str,
    last_name: Optional[str],
    username: Optional[str],
    current_city: str,
    current_country: str,
    current_occupation: Optional[str] = None,
    monthly_income: Optional[float] = None,
    currency: str = 'USD'
) -> bool:
    """Update or create user profile"""
    try:
        with get_user_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO bot.user_profiles (
                        user_id, username, first_name, last_name,
                        current_city, current_country, current_occupation,
                        monthly_income, currency
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE SET
                        username = EXCLUDED.username,
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        current_city = EXCLUDED.current_city,
                        current_country = EXCLUDED.current_country,
                        current_occupation = EXCLUDED.current_occupation,
                        monthly_income = EXCLUDED.monthly_income,
                        currency = EXCLUDED.currency
                """, (
                    user_id, username, first_name, last_name,
                    current_city, current_country, current_occupation,
                    monthly_income, currency
                ))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        return False

async def record_simulation(
    user_id: int,
    simulation_type: str,
    source_city: str,
    target_city: str,
    source_occupation: Optional[str] = None,
    target_occupation: Optional[str] = None
) -> bool:
    """Record a simulation in history"""
    try:
        with get_user_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO bot.simulations (
                        user_id, simulation_type, source_city,
                        target_city, source_occupation, target_occupation
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    user_id, simulation_type, source_city,
                    target_city, source_occupation, target_occupation
                ))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error recording simulation: {e}")
        return False

async def get_user_simulations(user_id: int, limit: int = 5) -> list:
    """Get user's recent simulations"""
    try:
        with get_user_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM bot.simulations 
                    WHERE user_id = %s 
                    ORDER BY simulated_at DESC 
                    LIMIT %s
                """, (user_id, limit))
                return cur.fetchall()
    except Exception as e:
        logger.error(f"Error fetching user simulations: {e}")
        return []
