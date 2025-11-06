from fastapi import APIRouter
from app.service.messages import get_group_messages, get_group_messages_and_threads

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.get("/{groupId}")
async def get_all_messages(groupId : str):
    return await get_group_messages(groupId)

@router.get("/{groupId}/threads")
async def get_all_messages_threads(groupId: str):
    return await get_group_messages_and_threads(groupId)