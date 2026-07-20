from fastapi import APIRouter

from services.progress import get_progress


router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)


@router.get("")
def progress_status():

    return get_progress()