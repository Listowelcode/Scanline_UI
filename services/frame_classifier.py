import json

from services.code_classifier import classify_code



def classify_frames(input_file):

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()



    # Split frames
    frames = content.split("--- FRAME")


    results = []


    for frame in frames:

        if frame.strip() == "":
            continue


        # separate frame number and text
        parts = frame.split("---", 1)


        if len(parts) < 2:
            continue


        frame_number = parts[0].strip()

        text = parts[1].strip()



        language = classify_code(
            text
        )


        results.append(
            {
                "frame": frame_number,
                "language": language,
                "text": text
            }
        )



    return results





def save_classified_frames(data):

    with open(
        "classified_frames.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )