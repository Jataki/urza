from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence, List, Dict, Optional, Union
from agents.strategist_agent import StrategistAgent
from agents.query_agent import QueryAgent
from utils.response_formatters import format_card_results
from config import GOOGLE_API_KEY, STRATEGIST_MODEL, QUERY_MODEL


# Define the state for the graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[Union[HumanMessage, AIMessage]], "Conversation messages"]
    strategy: Annotated[Optional[str], "Strategy recommendations"]
    queries: Annotated[Optional[List[str]], "Scryfall queries"]
    cards: Annotated[Optional[List[Dict]], "Card results"]
    session_id: Annotated[str, "Conversation session ID"]

class CardAdvisorWorkflow:
    """Workflow for the card advisor system."""
    
    def __init__(self, api_key=None):
        """Initialize the workflow with agents."""
        self.api_key = api_key or GOOGLE_API_KEY
        self.strategist = StrategistAgent(
            model_name=STRATEGIST_MODEL,
            api_key=self.api_key
        )
        self.query_agent = QueryAgent(
            model_name=QUERY_MODEL,
            api_key=self.api_key
        )
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Node 1: Generate strategy recommendations
        def generate_strategy(state: AgentState) -> AgentState:
            query = state["messages"][-1].content
            session_id = state["session_id"]
            strategy_result = self.strategist.process({
                "query": query,
                "session_id": session_id
            })
            return {"strategy": strategy_result["answer"]}
        
        # Node 2: Generate queries and fetch cards
        def fetch_cards(state: AgentState) -> AgentState:
            strategy = state["strategy"]
            query_result = self.query_agent.process({
                "strategy": strategy
            })
            return {
                "queries": query_result["queries"],
                "cards": query_result["cards"]
            }
        
        # Node 3: Prepare final response
        def prepare_response(state: AgentState) -> AgentState:
            strategy = state["strategy"]
            cards = state["cards"]
            print('hahaha')
            formatted_response = format_card_results(strategy, cards)
            final_message = AIMessage(content=formatted_response)
            print(final_message)
            return {"messages": state["messages"] + [final_message]}
        
        # Add nodes to the graph
        workflow.add_node("strategist", generate_strategy)
        workflow.add_node("card_fetcher", fetch_cards)
        workflow.add_node("response_builder", prepare_response)
        
        # Add edges to define the flow
        workflow.add_edge("strategist", "card_fetcher")
        workflow.add_edge("card_fetcher", "response_builder")
        workflow.add_edge("response_builder", END)
        
        # Set the entry point
        workflow.set_entry_point("strategist")
        
        return workflow.compile()
    
    def process_query(self, query: str, session_id: str = "default_session") -> str:
        """Process a user query through the workflow."""
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "strategy": None,
            "queries": None,
            "cards": None,
            "session_id": session_id
        }
        result = self.workflow.invoke(initial_state)
        return result["messages"][-1].content
    
    def reset_session(self, session_id: str):
        """Reset a conversation session."""
        self.strategist.reset_session(session_id)