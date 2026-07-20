import json
import os
from datetime import datetime


def create_metadata(
    folder,
    language,
    filename,
    video_title=""
):

    metadata = {

        "language": language,

        "main_file": filename,

        "video_title": video_title,

        "generated_at": datetime.now().isoformat()

    }


    path = os.path.join(
        folder,
        "project.json"
    )


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )


    return metadata