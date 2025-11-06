from fastapi import APIRouter, Query, Body
from schemas.bot_message import MessageBody
from app.service.bot import send_bot_message_to_user_chat

router = APIRouter(prefix="/bot", tags=["Bot"])

@router.post("/send-message-to-user-chat")
async def send_bot_message(botName: str =  Query(..., description="보낼 봇 이름"), body: MessageBody = Body(...)):
    return await send_bot_message_to_user_chat(botName, body.model_dump())