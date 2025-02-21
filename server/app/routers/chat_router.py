from fastapi import APIRouter, Depends
from databases.qdrant import get_qdrant, Qdrant
from services.chat_service import process_chat
from schemas.chat import ChatRequest, ChatResponse


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    qdrant: Qdrant = Depends(get_qdrant)
) -> ChatResponse:
    """
    Chat with the AI assistant
    
    Args:
        request: Chat request containing message history
        qdrant: Qdrant instance from dependency injection
        
    Returns:
        Agent's response text
    """
    response = await process_chat(request.messages, qdrant)
    return ChatResponse(response=response) 