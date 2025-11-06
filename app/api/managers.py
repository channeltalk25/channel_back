from fastapi import APIRouter
from app.service.managers import get_managers

router = APIRouter(prefix="/managers", tags=["Managers"])

@router.get("")
async def get_managers_info() :
    return await get_managers()