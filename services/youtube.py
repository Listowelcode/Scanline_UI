import yt_dlp
import os


def download_video(url: str):

    output_folder = "downloads"

    os.makedirs(output_folder, exist_ok=True)

    options = {
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "format": "mp4"
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return {
        "title": info["title"],
        "file": file_path
    }