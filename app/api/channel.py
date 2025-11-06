from fastapi import APIRouter
from app.service.channel import get_channel

router = APIRouter(prefix="/channel", tags=["Channel"])

@router.get("")
async def get_channel_info() :
    return await get_channel()