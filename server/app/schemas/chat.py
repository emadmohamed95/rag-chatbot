from typing import List, Literal
from pydantic import BaseModel


class Message(BaseModel):
    """Schema for a single message"""
    content: str
    sender: Literal["user", "ai"]


class ChatRequest(BaseModel):
    """Schema for chat requests"""
    messages: List[Message]


class ChatResponse(BaseModel):
    """Schema for chat responses"""
    response: str 