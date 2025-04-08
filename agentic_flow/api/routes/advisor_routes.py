from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from workflows.advisor_workflow import CardAdvisorWorkflow
from config import GOOGLE_API_KEY

# Create router
router = APIRouter()

# Initialize workflow (lazy initialization to avoid startup penalty)
_workflow = None

def get_workflow():
    """Dependency to get the workflow instance."""
    global _workflow
    if _workflow is None:
        _workflow = CardAdvisorWorkflow(api_key=GOOGLE_API_KEY)
    return _workflow

# Define request/response models
class QueryRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ResetRequest(BaseModel):
    session_id: str

class CardResponse(BaseModel):
    name: str
    mana_cost: str
    type_line: str
    oracle_text: str
    image_uri: str
    scryfall_uri: str
    rarity: str
    set_name: str

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    queries: List[str]
    cards: List[CardResponse]

# Define endpoints
@router.post("/api/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    workflow: CardAdvisorWorkflow = Depends(get_workflow)
):
    """Process a user query about MTG strategy and card suggestions."""
    session_id = request.session_id or "default_session"
    
    try:
        result = workflow.process_query(request.message, session_id)
        
        # In a production implementation, workflow.process_query would return
        # structured data that could be directly mapped to QueryResponse
        # This is a simplified version that assumes text parsing
        
        # For now, we're returning a simplified response
        return {
            "answer": result,
            "session_id": session_id,
            "queries": [],  # In production, these would be extracted from the result
            "cards": []     # In production, these would be extracted from the result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/api/reset")
async def reset_session(
    request: ResetRequest,
    workflow: CardAdvisorWorkflow = Depends(get_workflow)
):
    """Reset a conversation session."""
    try:
        workflow.reset_session(request.session_id)
        return {"status": "success", "session_id": request.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting session: {str(e)}")

# Advanced endpoint for direct Scryfall queries (optional)
@router.post("/api/advanced-search")
async def advanced_search(
    query: str,
    limit: int = 10,
    workflow: CardAdvisorWorkflow = Depends(get_workflow)
):
    """Perform a direct Scryfall search using the provided query."""
    try:
        # This would use the query agent's fetch_cards method directly
        cards = workflow.query_agent.fetch_cards([query], max_cards_per_query=limit)
        return {"cards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching cards: {str(e)}")