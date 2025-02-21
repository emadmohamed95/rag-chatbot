from typing import List, Any, Dict, Optional
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from settings import settings
from databases.qdrant import Qdrant
from langchain.tools.retriever import create_retriever_tool


class ChatbotAgent:
    def __init__(self, qdrant: Qdrant):
        """
        Initialize the chatbot agent with RAG capabilities
        
        Args:
            qdrant: Shared Qdrant instance for vector storage
        """
        self.vector_store = qdrant.get_vector_store()
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize tools
        self.tools = self._create_tools()
        
        # Create the agent
        self.agent = self._create_agent()
        
    def _create_tools(self) -> List[Tool]:
        """Create the tools available to the agent"""
        retriever = self.vector_store.as_retriever()
        retriever_tool = create_retriever_tool(
            retriever,
            "search_documents",
            "Search through uploaded documents for relevant information",
        )
        return [retriever_tool]
        
    def _create_agent(self):
        """Create the ReAct agent with the specified tools and prompt"""
        system_prompt = """You are a helpful AI assistant that has access to a knowledge base of documents.
            Use the search_documents tool to find relevant information when needed.
            Always be polite and professional in your responses.
            If you don't find relevant information in the documents, be honest about it.
            Base your responses primarily on the information found in the documents.
            Always use the search_documents tool to find relevant information before responding.
            """
        
        return create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=system_prompt
        )
        
    async def chat(
        self, 
        message: str, 
        history: Optional[List[HumanMessage | AIMessage]] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message and return the response
        
        Args:
            message: User's message
            history: Optional list of previous messages in LangChain format
            
        Returns:
            Dictionary containing the agent's response and any additional info
        """
        # Get agent response
        result = await self.agent.ainvoke({
            "messages": history + [("user", message)]
        })
        
        return result["messages"][-1].content
