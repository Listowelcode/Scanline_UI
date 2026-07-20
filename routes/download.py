from fastapi import APIRouter
from fastapi.responses import FileResponse
import os


router = APIRouter(
    prefix="/download",
    tags=["Download"]
)


@router.get("/{filename:path}")
def download_file(filename: str):


    # Convert URL slashes to system path

    filename = filename.replace(
        "/",
        os.sep
    )


    path = filename



    if os.path.exists(path):

        return FileResponse(
            path,
            filename=os.path.basename(path)
        )


    return {
        "error": "File not found",
        "path": path
    }