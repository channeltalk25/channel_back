from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.service.clustering import extract_qa_pairs

router = APIRouter(prefix="/clustering", tags=["Clustering"])

@router.post("")
async def cluster_questions(chat_data: List[Dict[str, Any]]):
    return extract_qa_pairs(chat_data)