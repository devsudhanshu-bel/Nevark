
from fastapi import APIRouter

router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)


@router.get("/")
async def get_memory():

    return {
        "message": "Memory endpoint working"
    }
