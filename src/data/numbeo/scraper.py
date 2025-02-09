# src/data/numbeo/scraper.py
from bs4 import BeautifulSoup
import requests
import unicodedata
import logging
import time
import random
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)

def clean_cost_value(cost_text: str) -> Optional[float]:
    """Clean and convert cost text to float"""
    try:
        cost = cost_text.replace(u'\xa0', unicodedata.normalize("NFKC", u'\xa0'))
        cost = cost.replace(',', '').strip(' $')
        return float(cost)
    except (ValueError, AttributeError) as e:
        logger.error(f"Error cleaning cost value '{cost_text}': {str(e)}")
        return None

def extract_costs(rows: List[BeautifulSoup]) -> List[Optional[float]]:
    """Extract costs from HTML rows"""
    costs = []
    for row in rows:
        try:
            cost_cell = row.find('td', {'class': 'priceValue'})
            if cost_cell:
                cost = clean_cost_value(cost_cell.text)
                costs.append(cost)
        except Exception as e:
            logger.error(f"Error extracting cost: {str(e)}")
            costs.append(None)
    return costs

# src/data/numbeo/scraper.py
async def scrape_city_data(city_name: str) -> Optional[Dict[str, List[float]]]:
    """Scrape cost data for a specific city"""
    city_name = city_name.title().replace(' ', '-')
    req_url = f'https://www.numbeo.com/cost-of-living/in/{city_name}?displayCurrency=USD'
    
    logger.info(f"Scraping data from: {req_url}")
    
    try:
        # Add random delay to avoid overwhelming the server
        time.sleep(random.uniform(1, 3))
        
        # Use headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(req_url, headers=headers)
        response.raise_for_status()
        
        page_soup = BeautifulSoup(response.text, 'html.parser')
        all_rows_html = page_soup.find_all('tr')

        if not all_rows_html:
            logger.error(f"No data rows found for {city_name}")
            return None

        # Extract data for each category
        data = {
            'restaurant': extract_costs(all_rows_html[2:10]),
            'market': extract_costs(all_rows_html[11:30]),
            'transportation': extract_costs(all_rows_html[31:39]),
            'utilities': extract_costs(all_rows_html[40:43]),
            'leisure': extract_costs(all_rows_html[44:47]),
            'clothing': extract_costs(all_rows_html[51:55]),
            'rent': extract_costs(all_rows_html[56:60])
        }

        # Log extracted data for debugging
        logger.debug(f"Extracted data for {city_name}: {data}")

        # Verify we have data
        if not any(data.values()):
            logger.error(f"No costs found for {city_name}")
            return None

        # Verify required fields
        required_fields = ['restaurant', 'market', 'transportation', 'utilities', 'rent']
        for field in required_fields:
            if not data.get(field):
                logger.warning(f"Missing {field} data for {city_name}")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for {city_name}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error scraping {city_name}: {str(e)}")
        return None
