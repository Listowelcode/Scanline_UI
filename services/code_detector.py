import cv2
import os
import pytesseract


# Tesseract installation path (Windows)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


CODE_KEYWORDS = [

    # Python
    "import",
    "from",
    "def",
    "class",
    "print",
    "return",

    # HTML
    "<html>",
    "<head>",
    "<body>",
    "<div>",
    "<form>",
    "<input>",
    "<button>",
    "<script>",
    "<style>",
    "<title>",

    # CSS
    "color",
    "margin",
    "padding",
    "display",
    "font",
    "background",

    # JavaScript
    "function",
    "const",
    "let",
    "var",
    "console",
    "document",

    # SQL
    "select",
    "insert",
    "update",
    "delete",
    "where",
    "from"
]


def detect_code_frames(
    frames_folder,
    output_folder,
    min_words=3,
    min_score=2
):

    os.makedirs(output_folder, exist_ok=True)

    saved = 0


    for image_name in os.listdir(frames_folder):

        image_path = os.path.join(
            frames_folder,
            image_name
        )


        image = cv2.imread(image_path)


        if image is None:
            continue



        # -------------------------
        # OCR PREPROCESSING
        # -------------------------

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )


        # Increase contrast
        gray = cv2.threshold(
            gray,
            150,
            255,
            cv2.THRESH_BINARY
        )[1]


        # Enlarge for OCR
        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2
        )


        # OCR
        text = pytesseract.image_to_string(
            gray,
            config="--psm 6"
        )


        text_lower = text.lower()

        words = text.split()



        # -------------------------
        # SCORING SYSTEM
        # -------------------------

        score = 0



        # Keyword checking
        for keyword in CODE_KEYWORDS:

            if keyword.lower() in text_lower:
                score += 1



        # Symbol checking
        symbols = [
            "<",
            ">",
            "{",
            "}",
            ";",
            "=",
            "(",
            ")",
            "/"
        ]


        for symbol in symbols:

            if symbol in text:
                score += 0.5



        # Line structure
        lines = text.split("\n")


        if len(lines) >= 5:
            score += 1



        # Code-like lines
        short_lines = 0


        for line in lines:

            if 5 <= len(line) <= 80:
                short_lines += 1


        if short_lines >= 3:
            score += 1



        # -------------------------
        # SAVE CODE FRAME
        # -------------------------

        if len(words) >= min_words and score >= min_score:


            save_path = os.path.join(
                output_folder,
                f"code_{saved:05d}.jpg"
            )


            cv2.imwrite(
                save_path,
                image
            )


            saved += 1



    return saved