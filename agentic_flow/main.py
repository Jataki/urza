from api.app import app
import uvicorn
from config import GOOGLE_API_KEY

if __name__ == "__main__":
    # Check API key is set
    if not GOOGLE_API_KEY:
        print("WARNING: GOOGLE_API_KEY environment variable is not set")
    
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)