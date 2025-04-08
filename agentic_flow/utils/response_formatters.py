from typing import Dict, List, Any

def format_card_results(strategy: str, cards: List[Dict[str, Any]]) -> str:
    """Format strategy and card results into a readable response."""
    # Group cards by their query
    cards_by_query = {}
    for card in cards:
        query = card.pop("query", "unknown")
        if query not in cards_by_query:
            cards_by_query[query] = []
        cards_by_query[query].append(card)
    
    # Build the response
    response = f"{strategy}\n\n## Cards That Match This Strategy:\n\n"
    
    for query, query_cards in cards_by_query.items():
        response += f"### Search: `{query}`\n\n"
        for card in query_cards:
            response += f"- **{card['name']}** ({card['mana_cost']}) - {card['type_line']}\n"
            response += f"  {card['oracle_text']}\n\n"
    
    return response