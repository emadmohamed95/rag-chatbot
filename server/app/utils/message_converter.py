from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from schemas.chat import Message


def to_langchain_messages(messages: List[Message]) -> List[HumanMessage | AIMessage]:
    """
    Convert API message models to LangChain message format
    
    Args:
        messages: List of API message models
        
    Returns:
        List of LangChain messages
    """
    return [
        AIMessage(content=msg.content) if msg.sender == "ai"
        else HumanMessage(content=msg.content)
        for msg in messages
    ] 