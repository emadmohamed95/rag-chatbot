from typing import List
from agents.chatbot_agent import ChatbotAgent
from databases.qdrant import Qdrant
from schemas.chat import Message
from utils.message_converter import to_langchain_messages


async def process_chat(
    messages: List[Message],
    qdrant: Qdrant
) -> str:
    """
    Process a chat request
    
    Args:
        messages: List of chat messages
        qdrant: Qdrant instance for vector storage
        
    Returns:
        Agent's response text
    """
    # Create agent with the shared Qdrant instance
    agent = ChatbotAgent(qdrant)
    
    # Convert messages to LangChain format (excluding the last message)
    history = to_langchain_messages(messages[:-1])
    
    # Get the latest message
    latest_message = messages[-1].content
    
    # Get response from agent
    result = await agent.chat(latest_message, history)
    return result