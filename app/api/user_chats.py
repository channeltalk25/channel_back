from fastapi import APIRouter, Query
from app.service.user_chats import get_all_user_chat_messages

router = APIRouter(prefix="/user-chats", tags=["User Chats"])

@router.get("")
async def get_user_chats(since: str = Query(..., description="Epoch time in milliseconds")):
    return await get_all_user_chat_messages(since)