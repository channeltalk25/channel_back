from fastapi import APIRouter, Query
from app.service.recommend import get_recommended_answers

router = APIRouter(prefix="/recommend", tags=["Recommend"])

@router.get("")
async def recommend_answers(question: str = Query(... , description="User Question")):
    print(question)
    return await get_recommended_answers(question)