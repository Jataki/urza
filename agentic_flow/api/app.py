from fastapi import FastAPI
from .routes import advisor_routes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MTG Card Advisor API",
    description="API for Magic: The Gathering strategy advice and card recommendations",
    version="1.0.0"
)

# Include routers from route modules
app.include_router(advisor_routes.router, tags=["advisor"])

# Health check endpoint
@app.get("/health", tags=["system"])
async def health_check():
    """System health check endpoint."""
    return {"status": "healthy"}