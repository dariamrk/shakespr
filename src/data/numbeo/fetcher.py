# src/data/numbeo/fetcher.py
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
from src.utils.database import get_numbeo_db_connection
from src.utils.logging import logger
from typing import Optional, Dict, Any

async def fetch_city_data(city_name: str, country: str) -> Optional[Dict[str, Any]]:
    """
    Fetch city data from local database first, if not found or outdated,
    fetch from Numbeo and store in database.
    """
    logger.info(f"Fetching data for {city_name}, {country}")
    
    # Try to get data from local database first
    local_data = await get_local_city_data(city_name, country)
    if local_data:
        logger.info(f"Found recent local data for {city_name}")
        return local_data

    # If no local data, fetch from Numbeo
    logger.info(f"No recent local data found for {city_name}, fetching from Numbeo")
    numbeo_data = await fetch_and_store_numbeo_data(city_name, country)
    return numbeo_data

async def get_local_city_data(city_name: str, country: str) -> Optional[Dict[str, Any]]:
    """Get city data from local PostgreSQL database"""
    try:
        with get_numbeo_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Check for recent data (last 30 days)
                cur.execute("""
                    WITH latest_update AS (
                        SELECT c.city_id, MAX(u.update_id) as update_id
                        FROM numbeo_col.cities c
                        JOIN numbeo_col.updates u ON c.city_id = u.city_id
                        WHERE LOWER(c.city_name) = LOWER(%s)
                        AND LOWER(c.country) = LOWER(%s)
                        AND u.date > NOW() - INTERVAL '30 days'
                        GROUP BY c.city_id
                    )
                    SELECT 
                        c.city_name,
                        c.country,
                        c.region,
                        r.cheap_meal_for_one,
                        m.milk_one_liter,
                        t.monthly_transit_pass,
                        ut.all_basic as utilities_basic,
                        rent.apt_one_bdrm_ctr as rent_1br_center,
                        u.date as last_updated
                    FROM latest_update lu
                    JOIN numbeo_col.cities c ON lu.city_id = c.city_id
                    JOIN numbeo_col.updates u ON lu.update_id = u.update_id
                    LEFT JOIN numbeo_col.restaurant_cost_sets r ON lu.update_id = r.update_id
                    LEFT JOIN numbeo_col.market_cost_sets m ON lu.update_id = m.update_id
                    LEFT JOIN numbeo_col.transportation_cost_sets t ON lu.update_id = t.update_id
                    LEFT JOIN numbeo_col.utilities_cost_sets ut ON lu.update_id = ut.update_id
                    LEFT JOIN numbeo_col.rent_cost_sets rent ON lu.update_id = rent.update_id
                    WHERE c.city_id = (
                        SELECT city_id FROM latest_update
                    )
                """, (city_name, country))
                
                result = cur.fetchone()
                return result

    except Exception as e:
        logger.error(f"Error getting local city data: {e}")
        return None

async def fetch_and_store_numbeo_data(city_name: str, country: str) -> Optional[Dict[str, Any]]:
    """Fetch data from Numbeo and store in local database"""
    try:
        # Import the scraper only when needed
        from src.data.numbeo.scraper import scrape_city_data
        
        # First, check if city exists in our database
        with get_numbeo_db_connection() as conn:
            with conn.cursor() as cur:
                # Try to get existing city_id first
                cur.execute("""
                    SELECT city_id 
                    FROM numbeo_col.cities 
                    WHERE LOWER(city_name) = LOWER(%s) 
                    AND LOWER(country) = LOWER(%s)
                """, (city_name, country))
                
                result = cur.fetchone()
                if result:
                    city_id = result[0]
                    logger.info(f"Found existing city_id: {city_id}")
                else:
                    # Create new city if it doesn't exist
                    cur.execute("""
                        INSERT INTO numbeo_col.cities (city_name, country, region)
                        VALUES (%s, %s, %s)
                        RETURNING city_id
                    """, (city_name, country, ''))
                    city_id = cur.fetchone()[0]
                    logger.info(f"Created new city with id: {city_id}")
                
                # Scrape data from Numbeo
                scraped_data = await scrape_city_data(city_name)
                if not scraped_data:
                    logger.error(f"Failed to scrape data for {city_name}")
                    return None
                
                logger.info(f"Scraped data: {scraped_data}")
                
                # Insert update record
                cur.execute("""
                    INSERT INTO numbeo_col.updates (city_id, date)
                    VALUES (%s, CURRENT_TIMESTAMP)
                    RETURNING update_id
                """, (city_id,))
                update_id = cur.fetchone()[0]
                logger.info(f"Created update record with id: {update_id}")
                
                # Insert cost data
                if 'restaurant' in scraped_data and scraped_data['restaurant']:
                    restaurant_data = scraped_data['restaurant']
                    logger.info(f"Restaurant data: {restaurant_data}")
                    try:
                        cur.execute("""
                            INSERT INTO numbeo_col.restaurant_cost_sets
                            (update_id, cheap_meal_for_one, meal_for_two, mcdonalds_meal,
                             domestic_beer, imported_beer, cappuccino, coke_or_pepsi, water)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (update_id, *restaurant_data[:8]))
                    except Exception as e:
                        logger.error(f"Error inserting restaurant data: {e}")

                # Similar blocks for other cost sets...
                
                conn.commit()
                logger.info("Successfully committed all data")
                
                # Return the newly scraped and stored data
                return await get_local_city_data(city_name, country)

    except Exception as e:
        logger.error(f"Error fetching and storing Numbeo data: {e}", exc_info=True)
        return None
