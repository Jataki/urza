import requests
from typing import Dict, List, Any, Optional
import time
import logging

logger = logging.getLogger(__name__)

class ScryfallService:
    """Service for interacting with the Scryfall API."""
    
    BASE_URL = "https://api.scryfall.com"
    
    # Cache to avoid repetitive API calls
    _cache = {}
    _cache_timeout = 3600  # 1 hour cache timeout
    _cache_timestamp = {}
    
    # Rate limiting settings
    _last_request_time = 0
    _min_request_interval = 0.1  # 100ms between requests to be courteous
    
    @classmethod
    def search_cards(cls, query: str, order: str = "edhrec", unique: str = "cards", 
                     max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search for cards using the Scryfall API.
        
        Args:
            query: The search query in Scryfall syntax
            order: How to order the results (e.g., "edhrec", "name", "released")
            unique: The uniqueness strategy ("cards", "art", "prints")
            max_results: Maximum number of results to return
            
        Returns:
            List of card objects
        """
        # Create cache key
        cache_key = f"{query}_{order}_{unique}"
        
        # Check cache first
        if cache_key in cls._cache:
            cache_time = cls._cache_timestamp.get(cache_key, 0)
            if time.time() - cache_time < cls._cache_timeout:
                logger.debug(f"Cache hit for query: {query}")
                cards = cls._cache[cache_key]
                return cards[:max_results] if max_results else cards
        
        # Implement rate limiting
        cls._rate_limit()
        
        params = {
            "q": query,
            "order": order,
            "unique": unique
        }
        
        try:
            logger.info(f"Searching Scryfall for: {query}")
            response = requests.get(f"{cls.BASE_URL}/cards/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            cards = data.get("data", [])
            
            # Update cache
            cls._cache[cache_key] = cards
            cls._cache_timestamp[cache_key] = time.time()
            
            # Limit results if needed
            if max_results is not None:
                return cards[:max_results]
                
            return cards
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"No cards found for query: {query}")
                return []
            logger.error(f"HTTP error searching Scryfall: {e}")
            raise
        except requests.RequestException as e:
            logger.error(f"Error searching Scryfall: {e}")
            raise
    
    @classmethod
    def get_card(cls, card_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific card by its Scryfall ID."""
        # Implement rate limiting
        cls._rate_limit()
        
        try:
            response = requests.get(f"{cls.BASE_URL}/cards/{card_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching card {card_id}: {e}")
            return None
    
    @classmethod
    def _rate_limit(cls):
        """Implement rate limiting to be courteous to the Scryfall API."""
        current_time = time.time()
        time_since_last_request = current_time - cls._last_request_time
        
        if time_since_last_request < cls._min_request_interval:
            sleep_time = cls._min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        cls._last_request_time = time.time()