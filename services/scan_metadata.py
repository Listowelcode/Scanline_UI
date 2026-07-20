import json
import os
from datetime import datetime



def save_metadata(
    scan_folder,
    scan_id,
    title,
    url,
    status,
    zip_file=None
):


    metadata = {

        "scan_id": scan_id,

        "title": title,

        "url": url,

        "created": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "status": status,

        "zip_file": (
            zip_file.replace("\\", "/")
            if zip_file
            else None
        )

    }



    path = os.path.join(
        scan_folder,
        "metadata.json"
    )



    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )



    return path