from fastapi import APIRouter
from app.service.threads import get_message_threads

router = APIRouter(prefix="/threads", tags=["Threads"])

@router.get("/{groupId}/{messageId}")
async def get_message_thread_history(groupId: str, messageId: str):
    return await get_message_threads(groupId, messageId)