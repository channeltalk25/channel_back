from fastapi import APIRouter, Query
from typing import Optional
from app.service.chats import get_all_user_chat_messages

router = APIRouter(prefix="/user-chats", tags=["User Chats"])

@router.get("")
async def get_user_chats(since: str = Query(1762239127019, description="Epoch time in milliseconds")):
    return await get_all_user_chat_messages(since)