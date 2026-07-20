from fastapi import APIRouter
import os
import json


router = APIRouter(
    prefix="/scans",
    tags=["Scan History"]
)


@router.get("")
def get_scan_history():

    scans = []

    scans_folder = "scans"


    if not os.path.exists(scans_folder):

        return scans


    for scan_id in os.listdir(scans_folder):

        scan_path = os.path.join(
            scans_folder,
            scan_id
        )


        metadata_path = os.path.join(
            scan_path,
            "metadata.json"
        )


        if os.path.exists(metadata_path):

            with open(
                metadata_path,
                "r",
                encoding="utf-8"
            ) as file:

                metadata = json.load(file)

                scans.append(
                    metadata
                )


    return scans