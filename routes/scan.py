from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from services.pipeline import run_pipeline
from services.progress import update_progress, set_status
from services.url_validator import is_valid_youtube_url


router = APIRouter(
    prefix="/scan",
    tags=["ScanLine"]
)


class ScanRequest(BaseModel):

    youtube_url: str



def start_pipeline(url):

    try:

        set_status(
            "processing"
        )


        output_file = run_pipeline(
            url
        )


        update_progress(
            100,
            "Extraction Complete!",
            output_file
        )


        set_status(
            "completed"
        )


    except Exception as e:

        set_status(
            "failed"
        )


        update_progress(
            -1,
            f"Error: {str(e)}"
        )




@router.post("")
def scan_video(
    request: ScanRequest,
    background_tasks: BackgroundTasks
):

    # ---------------------------------
    # Validate YouTube URL
    # ---------------------------------

    if not is_valid_youtube_url(
        request.youtube_url
    ):

        return {

            "status": "error",

            "message": "Please enter a valid YouTube URL."

        }


    update_progress(
        0,
        "Starting scan..."
    )


    set_status(
        "processing"
    )


    background_tasks.add_task(
        start_pipeline,
        request.youtube_url
    )


    return {

        "status": "started",

        "message": "Scan pipeline started"

    }