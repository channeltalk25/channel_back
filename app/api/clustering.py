from fastapi import APIRouter, Query
from app.service.clustering import get_clusters
from app.service.chats import get_all_user_chat_messages

router = APIRouter(prefix="/clustering", tags=["Clustering"])

@router.get("")
async def cluster_questions(since: str = Query(1762239127019, description="Epoch time in milliseconds")):
    chat_data = await get_all_user_chat_messages(since)
    return await get_clusters(chat_data)