from fastapi import APIRouter
from typing import List, Dict, Any
from app.service.clustering import get_clusters

router = APIRouter(prefix="/clustering", tags=["Clustering"])

@router.post("")
async def cluster_questions(chat_data: List[Dict[str, Any]]):
    return await get_clusters(chat_data)