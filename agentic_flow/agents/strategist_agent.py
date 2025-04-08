from typing import Dict, Any, Optional
from .base_agent import Agent
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from services.knowledge_service import KnowledgeBaseRetriever
from prompts.strategist_prompts import get_context_prompt, get_mtg_strategist_prompt
from config import STRATEGIST_MODEL, GOOGLE_API_KEY

class StrategistAgent(Agent):
    """Agent responsible for providing MTG strategy recommendations."""
    
    def __init__(self, model_name=None, temperature=0.7, api_key=None):
        """Initialize the strategist agent."""
        model_name = model_name or STRATEGIST_MODEL
        api_key = api_key or GOOGLE_API_KEY
        super().__init__(model_name, temperature, api_key)
        self.knowledge_retriever = KnowledgeBaseRetriever().initialize().get_retriever()
        self.chain = self._build_chain()
        self.store = {}

    def _build_chain(self):
        """Build the history-aware retrieval chain."""
        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            self.llm, 
            self.knowledge_retriever, 
            get_context_prompt()
        )
        
        # Create document chain
        question_answer_chain = create_stuff_documents_chain(
            self.llm, 
            get_mtg_strategist_prompt()
        )
        
        # Create retrieval chain
        rag_chain = create_retrieval_chain(
            history_aware_retriever, 
            question_answer_chain
        )
        
        return RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user query using the agent chain."""
        query = input_data.get("query")
        session_id = input_data.get("session_id", "default_session")
        
        response = self.chain.invoke(
            {"input": query},
            {"configurable": {"session_id": session_id}}
        )
        
        return response
    
    def get_session_history(self, session_id: str):
        """Get or create chat history for the session."""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    def reset_session(self, session_id: str):
        """Reset the conversation history for a session."""
        if session_id in self.store:
            self.store[session_id].clear()