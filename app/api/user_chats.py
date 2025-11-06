from fastapi import APIRouter
from app.service.user_chats import get_user_chatIds, get_user_chat_messages, get_all_user_chat_messages

router = APIRouter(prefix="/user-chats", tags=["User Chats"])

@router.get("")
async def get_user_chats() :
    return await get_all_user_chat_messages()

# @router.get("/ids")
# async def get_user_chats_ids() :
#     return await get_user_chatIds()

# @router.get("/{chatId}/messages")
# async def get_user_chat_history(chatId :str) :
#     return await get_user_chat_messages(chatId)