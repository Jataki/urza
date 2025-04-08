from typing import Dict, Any, List, Optional
import json
import re
from .base_agent import Agent
from langchain_core.messages import HumanMessage, SystemMessage
from prompts.query_prompts import get_query_generation_prompt
from services.scryfall_service import ScryfallService
from config import QUERY_MODEL, GOOGLE_API_KEY

class QueryAgent(Agent):
    """Agent responsible for converting strategy into Scryfall search queries."""
    
    def __init__(self, model_name=None, temperature=0.2, api_key=None):
        """Initialize the query agent."""
        model_name = model_name or QUERY_MODEL
        api_key = api_key or GOOGLE_API_KEY
        super().__init__(model_name, temperature, api_key)
        self.scryfall_service = ScryfallService()
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process strategy recommendations and return card results."""
        strategy = input_data.get("strategy", "")
        
        # Generate Scryfall search queries
        queries = self.generate_queries(strategy)

        # Fetch cards from Scryfall API using the service
        cards = self.fetch_cards(queries)
        
        return {
            "queries": queries,
            "cards": cards
        }
    
    def generate_queries(self, strategy: str) -> List[str]:
        """Generate Scryfall search queries from strategy recommendations."""
        prompt = get_query_generation_prompt()
        messages = [
            SystemMessage(content=prompt["system"]),
            HumanMessage(content=prompt["user"].format(recommendations=strategy))
        ]
        
        response = self.llm.invoke(messages)
        print(response)
        try:
            return self._parse_queries(response.content)
        except Exception as e:
            print(f"Error parsing queries: {e}")
            return []
    
    def fetch_cards(self, queries: List[str], max_cards_per_query: int = 5) -> List[Dict[Any, Any]]:
        """Fetch cards from Scryfall API based on generated queries."""
        all_cards = []
        for query in queries:
            try:
                # Use the ScryfallService to fetch cards
                cards = self.scryfall_service.search_cards(
                    query=query, 
                    order="edhrec", 
                    unique="cards",
                    max_results=max_cards_per_query
                )
                
                # Process each card to extract relevant information
                for card in cards:
                    card_info = self._extract_card_info(card, query)
                    all_cards.append(card_info)
                    
            except Exception as e:
                print(f"Error fetching cards for query '{query}': {e}")
        
        return all_cards
    
    def _extract_card_info(self, card: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Extract relevant card information."""
        # Get image URI safely handling double-faced cards
        image_uri = ""
        if "image_uris" in card:
            image_uri = card["image_uris"].get("normal", "")
        elif "card_faces" in card and len(card["card_faces"]) > 0:
            image_uri = card["card_faces"][0].get("image_uris", {}).get("normal", "")
        
        return {
            "name": card.get("name", ""),
            "mana_cost": card.get("mana_cost", ""),
            "type_line": card.get("type_line", ""),
            "oracle_text": card.get("oracle_text", ""),
            "image_uri": image_uri,
            "scryfall_uri": card.get("scryfall_uri", ""),
            "rarity": card.get("rarity", ""),
            "set_name": card.get("set_name", ""),
            "query": query
        }
    
    def _parse_queries(self, queries_text: str) -> List[str]:
        """Parse the LLM response to extract Scryfall queries."""
        try:
            # Try to extract a JSON array
            json_match = re.search(r'\[(.*?)\]', queries_text, re.DOTALL)
            if json_match:
                json_str = f"[{json_match.group(1)}]"
                return json.loads(json_str)
            
            # If that fails, try the whole text
            return json.loads(queries_text)
        except json.JSONDecodeError:
            # Fallback to line-by-line extraction
            lines = queries_text.strip().split('\n')
            queries = []
            
            for line in lines:
                # Clean up common prefixes
                clean_line = re.sub(r'^[\s\d\."\'`-]*', '', line).strip()
                if clean_line and not clean_line.startswith('#') and len(clean_line) > 5:
                    queries.append(clean_line)
            
            return queries