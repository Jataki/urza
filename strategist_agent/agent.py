from google import genai
from retriever import KnowledgeBaseRetriever
from prompts import get_mtg_strategist_prompt, get_context_prompt
from config import GOOGLE_API_KEY, MODEL_NAME, TEMPERATURE
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory

class StrategistAgent:
    def __init__(self):        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME, 
            temperature=TEMPERATURE, 
            google_api_key=GOOGLE_API_KEY
        )
        
        # Initialize retriever
        self.base_retriever = KnowledgeBaseRetriever().initialize().get_retriever()
        
        # Build the chain
        self.chain = self._build_chain()

        # Statefully manage chat history
        self.store = {}

        
    def _build_chain(self):
        """Build the history-aware retrieval chain"""
        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(
            self.llm, 
            self.base_retriever, 
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
    
    def process_query(self, query, session_id="default_session"):
        """Process a user query using the agent chain"""
        response = self.chain.invoke(
            {"input": query},
            {"configurable": {"session_id": session_id}}
        )
        
        return response
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.chat_history.clear()

    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
