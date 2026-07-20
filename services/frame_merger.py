import re


def remove_duplicates(frames):

    unique_frames = []

    previous = ""


    for frame in frames:

        # remove extra spaces
        cleaned = re.sub(
            r"\s+",
            " ",
            frame
        ).strip()


        # compare with previous frame
        if cleaned != previous:

            unique_frames.append(frame)

            previous = cleaned


    return unique_frames



def merge_frames(frame_blocks):

    merged = ""


    for block in frame_blocks:

        merged += "\n"
        merged += block


    return merged