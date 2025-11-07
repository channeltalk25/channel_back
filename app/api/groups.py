from fastapi import APIRouter
from app.service.groups import get_groups
import time

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("")
async def get_groups_info() :
    return await get_groups()