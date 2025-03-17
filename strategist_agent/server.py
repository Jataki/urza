# strategist_agent/server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from agent import StrategistAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
agent = StrategistAgent()

class QueryRequest(BaseModel):
    message: str
    session_id: str | None = None

class ResetRequest(BaseModel):
    session_id: str

@app.post("/api/query")
async def process_query(request: QueryRequest):
    try:
        response = agent.process_query(request.message, request.session_id)
        return {
            "answer": response["answer"],
            "session_id": request.session_id or "default_session"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
async def reset_conversation(request: ResetRequest):
    try:
        agent.get_session_history(request.session_id).clear()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)