import cv2
import os
import numpy as np


# --------------------------------------------------
# FIND LATEST VIDEO
# --------------------------------------------------

def get_latest_video(folder):
    """
    Finds the newest video file inside a folder.
    """

    files = os.listdir(folder)

    videos = [
        f for f in files
        if f.lower().endswith(
            (".mp4", ".webm", ".mkv")
        )
    ]

    if not videos:
        return None


    latest = max(
        videos,
        key=lambda f: os.path.getmtime(
            os.path.join(folder, f)
        )
    )

    return os.path.join(
        folder,
        latest
    )



# --------------------------------------------------
# FRAME SIMILARITY
# --------------------------------------------------

def frame_similarity(frame1, frame2):
    """
    Checks how similar two frames are.
    """

    small1 = cv2.resize(
        frame1,
        (320, 180)
    )

    small2 = cv2.resize(
        frame2,
        (320, 180)
    )


    difference = cv2.absdiff(
        small1,
        small2
    )


    score = np.mean(
        difference
    )


    similarity = 1 - (
        score / 255
    )


    return similarity



# --------------------------------------------------
# FRAME EXTRACTION
# --------------------------------------------------

def extract_frames(
        video_path,
        output_folder,
        interval=1,
        similarity_threshold=0.98
):

    """
    Extract frames for coding tutorials.

    Keeps frames at intervals,
    removes only near-identical frames.
    """


    os.makedirs(
        output_folder,
        exist_ok=True
    )


    cap = cv2.VideoCapture(
        video_path
    )


    if not cap.isOpened():

        print(
            "Could not open video"
        )

        return 0



    fps = cap.get(
        cv2.CAP_PROP_FPS
    )


    if fps == 0:

        print(
            "Could not read FPS"
        )

        return 0



    frame_interval = max(
        int(fps * interval),
        1
    )



    count = 0
    saved = 0


    previous_saved_frame = None



    while True:


        ret, frame = cap.read()


        if not ret:
            break



        if count % frame_interval == 0:



            save_frame = True



            if previous_saved_frame is not None:


                similarity = frame_similarity(
                    frame,
                    previous_saved_frame
                )


                # Only remove almost identical frames

                if similarity >= similarity_threshold:

                    save_frame = False



            if save_frame:


                filename = os.path.join(
                    output_folder,
                    f"frame_{saved:05d}.jpg"
                )


                cv2.imwrite(
                    filename,
                    frame
                )


                previous_saved_frame = frame.copy()


                saved += 1



        count += 1



    cap.release()


    return saved