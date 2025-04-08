from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY


class Agent(ABC):
    """Base class for all card advisor agents."""
    
    def __init__(self, model_name: str, temperature: float = 0.7, api_key: Optional[str] = None):
        """Initialize the agent with LLM configuration."""
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key or GOOGLE_API_KEY
        self.llm = self._init_llm()
    
    def _init_llm(self) -> ChatGoogleGenerativeAI:
        """Initialize the language model."""
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=self.api_key
        )
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results."""
        pass