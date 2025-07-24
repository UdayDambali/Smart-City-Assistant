from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple, Optional
from app.services.granite_llm import generate_chat_response

router = APIRouter()

# Define request schema
class ChatRequest(BaseModel):
    user_input: str
    chat_history: Optional[List[Tuple[str, str]]] = None

# Define endpoint
@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    reply = generate_chat_response(payload.user_input, chat_history=payload.chat_history)
    return {"response": str(reply)}  # force wrap it as string in JSON response


