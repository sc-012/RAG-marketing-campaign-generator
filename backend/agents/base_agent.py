"""
Base Agent class for all marketing agents
"""
from crewai import Agent
from typing import Dict, Any, List
import os

class BaseMarketingAgent:
    """Base class for all marketing agents"""
    
    def __init__(self, name: str, role: str, goal: str, backstory: str, 
                 tools: List = None, llm=None, verbose: bool = True):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.llm = llm
        self.verbose = verbose
        
    def create_agent(self) -> Agent:
        """Create and return a CrewAI Agent instance - SIMPLIFIED VERSION"""
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=[],  # Disable tools to avoid delegation errors
            llm=self.llm,
            verbose=False,  # Reduce verbosity for cleaner output
            allow_delegation=False  # Disable delegation to avoid tool errors
        )
    
    def process_document_context(self, document_context: str) -> Dict[str, Any]:
        """Process document context and extract relevant information"""
        # This will be implemented by each specialized agent
        pass
    
    def generate_output(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agent-specific output"""
        # This will be implemented by each specialized agent
        pass
