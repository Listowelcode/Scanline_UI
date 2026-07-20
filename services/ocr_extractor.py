import cv2
import os
import pytesseract
import difflib
import numpy as np


# --------------------------------------------------
# TESSERACT CONFIGURATION
# --------------------------------------------------

# Windows path
windows_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(windows_tesseract):
    pytesseract.pytesseract.tesseract_cmd = windows_tesseract


# --------------------------------------------------
# IMAGE PREPROCESSING
# --------------------------------------------------

def preprocess_image(image):
    """
    Creates multiple enhanced versions of the frame
    for better OCR accuracy.
    """

    processed_images = []


    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    processed_images.append(gray)



    # Upscaled version
    upscale = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    processed_images.append(upscale)



    # Sharpen image
    kernel = np.array(
        [
            [0,-1,0],
            [-1,5,-1],
            [0,-1,0]
        ]
    )

    sharpened = cv2.filter2D(
        upscale,
        -1,
        kernel
    )

    processed_images.append(sharpened)



    # Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        sharpened,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    processed_images.append(adaptive)



    # OTSU threshold
    _, otsu = cv2.threshold(
        sharpened,
        0,
        255,
        cv2.THRESH_BINARY +
        cv2.THRESH_OTSU
    )

    processed_images.append(otsu)


    return processed_images



# --------------------------------------------------
# OCR WITH CONFIDENCE
# --------------------------------------------------

def run_ocr(image):

    results = []


    configs = [
        "--psm 6",
        "--psm 11"
    ]


    for config in configs:

        data = pytesseract.image_to_data(
            image,
            config=config,
            output_type=pytesseract.Output.DICT
        )


        words = []
        confidence_scores = []


        for i, word in enumerate(data["text"]):

            if word.strip():

                words.append(word)

                try:
                    confidence_scores.append(
                        int(data["conf"][i])
                    )

                except:
                    pass



        if words:

            text = " ".join(words)


            if confidence_scores:

                confidence = sum(
                    confidence_scores
                ) / len(confidence_scores)

            else:
                confidence = 0



            results.append(
                (
                    text,
                    confidence
                )
            )



    if not results:
        return "", 0



    # Return highest confidence result

    best = max(
        results,
        key=lambda x:x[1]
    )


    return best



# --------------------------------------------------
# DUPLICATE DETECTION
# --------------------------------------------------

def is_similar(new_text, existing_texts):

    for old in existing_texts:

        similarity = difflib.SequenceMatcher(
            None,
            new_text,
            old
        ).ratio()


        if similarity > 0.85:
            return True


    return False



# --------------------------------------------------
# MAIN OCR FUNCTION
# --------------------------------------------------

def extract_code_text(frames_folder):

    extracted_text = []


    frames = sorted(
        os.listdir(frames_folder)
    )


    for image_name in frames:


        image_path = os.path.join(
            frames_folder,
            image_name
        )


        image = cv2.imread(
            image_path
        )


        if image is None:
            continue



        # Generate OCR versions

        processed_versions = preprocess_image(
            image
        )


        best_text = ""
        best_confidence = 0



        # Run OCR on every version

        for processed in processed_versions:


            text, confidence = run_ocr(
                processed
            )


            if confidence > best_confidence:

                best_confidence = confidence
                best_text = text



        best_text = best_text.strip()



        # Ignore weak results

        if not best_text:
            continue


        if best_confidence < 40:
            continue



        # Remove similar duplicates

        if not is_similar(
            best_text,
            extracted_text
        ):

            extracted_text.append(
                best_text
            )



    return extracted_text