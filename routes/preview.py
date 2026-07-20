from fastapi import APIRouter
from pydantic import BaseModel

import yt_dlp

from services.url_validator import is_valid_youtube_url


router = APIRouter()


class PreviewRequest(BaseModel):

    youtube_url: str



@router.post("/preview")
def preview_video(data: PreviewRequest):


    # ---------------------------------
    # Validate URL format
    # ---------------------------------

    if not is_valid_youtube_url(
        data.youtube_url
    ):

        return {

            "status": "error",

            "message": "Please enter a valid YouTube URL."

        }



    ydl_opts = {

        "quiet": True,

        "skip_download": True

    }



    try:

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:


            info = ydl.extract_info(

                data.youtube_url,

                download=False

            )



        return {

            "status": "success",

            "title": info.get(
                "title"
            ),

            "channel": info.get(
                "uploader"
            ),

            "duration": info.get(
                "duration"
            ),

            "thumbnail": info.get(
                "thumbnail"
            ),

            "url": data.youtube_url

        }



    except Exception:

        return {

            "status": "error",

            "message": "Video not found or unavailable."

        }