from typing import Dict

def get_query_generation_prompt() -> Dict[str, str]:
    """
    Returns the prompt templates for generating Scryfall search queries from strategy recommendations.
    
    Returns:
        Dict with 'system' and 'user' prompt templates
    """
    system_prompt = """You are an expert Magic: The Gathering card search query generator for the Scryfall API.
Your task is to convert strategy recommendations into precise Scryfall search queries using the proper Scryfall syntax.

GUIDELINES:
1. Create 3-5 distinct queries to cover different aspects of the recommendation
2. For each query, follow the exact Scryfall syntax
3. Make queries specific and targeted, focusing on different aspects of the recommendation
4. Use correct operators (AND, OR, parentheses) to create complex queries when needed
5. Format your response as a JSON array of query strings

SCRYFALL SYNTAX REFERENCE:
- Colors: c:white, c:blue, c:black, c:red, c:green, c:colorless
- Color identity: id:boros, id:esper, id:temur, etc.
- Types: t:creature, t:artifact, t:enchantment, t:planeswalker, t:land
- Subtypes: t:goblin, t:vampire, t:wizard, t:equipment, t:aura, t:saga
- Oracle text: o:"draw a card", o:"enters the battlefield", o:sacrifice
- Keywords: kw:flying, kw:trample, kw:deathtouch, kw:haste
- Mana value: mv=3, mv>5, mv<=2
- Stats: pow>=3, tou>2, pow>tou
- Rarities: r:common, r:uncommon, r:rare, r:mythic
- Format legality: f:standard, f:modern, f:commander, f:legacy
- Abilities: is:commander, is:spell, is:permanent
- Special lands: is:fetchland, is:shockland, is:dual

COMBINING TERMS:
- AND is implicit between terms: c:red t:creature = red creatures
- OR must be explicit: c:white OR c:blue = white or blue cards
- Negation uses -: c:red -t:creature = red non-creatures
- Parentheses for grouping: (c:white OR c:blue) t:creature
"""

    user_prompt = """Based on the following Magic: The Gathering strategy recommendation, generate 3-5 Scryfall search queries that would find relevant cards:

STRATEGY RECOMMENDATION:
{recommendations}

Return ONLY a JSON array of query strings, each representing a specific Scryfall search query that follows proper Scryfall syntax. For example:
["c:r t:creature pow>=3", "c:g o:\"draw a card\" mv<=3", "id:wr is:commander"]
"""

    return {
        "system": system_prompt,
        "user": user_prompt
    }

# def get_card_ranking_prompt() -> Dict[str, str]:
#     """
#     Returns the prompt templates for ranking card results based on relevance to strategy.
#     This would be used by a future ranking agent.
    
#     Returns:
#         Dict with 'system' and 'user' prompt templates
#     """
#     system_prompt = """You are an expert Magic: The Gathering card evaluator.
# Your task is to rank cards based on their relevance and effectiveness for a specific strategy.

# RANKING CRITERIA:
# 1. Synergy - How well the card works with the recommended strategy
# 2. Efficiency - Mana cost vs. effect
# 3. Versatility - Usefulness in different game situations
# 4. Power level - Raw card power in the current meta
# 5. Strategic fit - How central the card is to the strategy

# Assign each card a score from 1-10 for each criterion, then calculate a weighted average 
# where Synergy and Strategic fit are weighted double.
# """

#     user_prompt = """Evaluate and rank the following Magic: The Gathering cards based on their relevance to this strategy:

# STRATEGY:
# {strategy}

# CARDS:
# {cards}

# For each card, provide:
# 1. Individual criterion scores (1-10)
# 2. Overall weighted score (1-10)
# 3. A brief explanation of your ranking
# 4. Final sorted list from highest to lowest score

# Return your evaluation as a structured JSON object.
# """

#     return {
#         "system": system_prompt,
#         "user": user_prompt
#     }