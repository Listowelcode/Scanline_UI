import os
import uuid

from services.youtube import download_video
from services.frame_extractor import extract_frames
from services.ocr_extractor import extract_code_text
from services.ai_cleaner import clean_code
from services.project_generator import generate_project
from services.zip_generator import create_zip
from services.scan_metadata import save_metadata

from services.progress import update_progress



def run_pipeline(url):

    print("=" * 50)
    print("SCANLINE PIPELINE STARTED")
    print("=" * 50)


    # ---------------------------------
    # CREATE SCAN SESSION
    # ---------------------------------

    scan_id = str(uuid.uuid4())[:8]


    scan_folder = os.path.join(
        "scans",
        scan_id
    )


    os.makedirs(
        scan_folder,
        exist_ok=True
    )


    save_metadata(
        scan_folder,
        scan_id,
        "Processing",
        url,
        "processing"
    )



    update_progress(
        0,
        "Pipeline started"
    )



    # ---------------------------------
    # STEP 1
    # DOWNLOAD VIDEO
    # ---------------------------------

    print("\n[1/6] Downloading video...")


    update_progress(
        10,
        "Downloading video"
    )


    video = download_video(
        url
    )


    video_path = video["file"]


    video_title = video.get(
        "title",
        "ScanLine_Project"
    )


    print(
        "Downloaded:",
        video_path
    )


    print(
        "Tutorial:",
        video_title
    )



    # ---------------------------------
    # STEP 2
    # EXTRACT FRAMES
    # ---------------------------------

    print("\n[2/6] Extracting frames...")


    update_progress(
        30,
        "Extracting frames"
    )


    frames_folder = os.path.join(
        scan_folder,
        "frames"
    )


    extract_frames(
        video_path,
        frames_folder
    )



    # ---------------------------------
    # STEP 3
    # OCR
    # ---------------------------------

    print("\n[3/6] Running OCR...")


    update_progress(
        50,
        "Extracting code from frames"
    )


    code = extract_code_text(
        frames_folder
    )


    ocr_text = ""


    for i, block in enumerate(code):

        ocr_text += f"""

--- FRAME {i} ---

{block}

"""



    extracted_file = os.path.join(
        scan_folder,
        "extracted_code.txt"
    )


    with open(
        extracted_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            ocr_text
        )



    print(
        "OCR saved"
    )



    # ---------------------------------
    # STEP 4
    # AI CLEANUP
    # ---------------------------------

    print("\n[4/6] Cleaning code using AI...")


    update_progress(
        70,
        "Cleaning code using AI"
    )


    cleaned = clean_code(
        ocr_text
    )



    cleaned_file = os.path.join(
        scan_folder,
        "cleaned_code.txt"
    )


    with open(
        cleaned_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            cleaned
        )



    print(
        "AI cleanup complete"
    )



    # ---------------------------------
    # STEP 5
    # GENERATE PROJECT
    # ---------------------------------

    print("\n[5/6] Generating project...")


    update_progress(
        85,
        "Generating project files"
    )


    folder = generate_project(
        cleaned,
        scan_folder
    )


    print(
        "Project created:",
        folder
    )



    # ---------------------------------
    # STEP 6
    # CREATE ZIP
    # ---------------------------------

    print("\n[6/6] Creating ZIP...")


    update_progress(
        95,
        "Creating ZIP file"
    )


    zip_file = create_zip(
        folder,
        video_title,
        scan_folder
    )


    print(
        "ZIP created:",
        zip_file
    )



    # ---------------------------------
    # COMPLETE
    # ---------------------------------

    save_metadata(
        scan_folder,
        scan_id,
        video_title,
        url,
        "completed",
        zip_file
    )


    update_progress(
        100,
        "Extraction Complete!",
        zip_file
    )


    print(
        "\nSCANLINE FINISHED!"
    )


    return zip_file