import re


# --------------------------------------------------
# COMMON OCR CODE CORRECTIONS
# --------------------------------------------------

OCR_FIXES = {

    # JavaScript / general programming
    "functlon": "function",
    "Functlon": "Function",
    "retum": "return",
    "Retum": "Return",
    "const1": "const",
    "Iet": "let",
    "varl": "var",

    # HTML
    "<d1v": "<div",
    "</d1v>": "</div>",
    "<p1": "<p",
    "<scrlpt": "<script",
    "</scrlpt>": "</script>",

    # CSS
    "co1or": "color",
    "backgound": "background",

    # Symbols OCR often damages
    "=>": "=>",
    "== =": "===",
    "= =": "==",

}



# --------------------------------------------------
# REMOVE UI NOISE
# --------------------------------------------------

IGNORE_PATTERNS = [

    # VS Code UI
    r"Visual Studio Code",
    r"Explorer",
    r"Extensions",
    r"Problems",
    r"Output",
    r"Terminal",
    r"Source Control",
    r"Run and Debug",

    # VS Code status bar
    r"UTF-8",
    r"CRLF",
    r"Ln\s*\d+",
    r"Col\s*\d+",
    r"Spaces",

    # Browser/UI noise
    r"YouTube",
    r"Gmail",
    r"Google",
    r"Search",

    # Common popup text
    r"Trust",
    r"Manage",
    r"Learn More",
]



# --------------------------------------------------
# APPLY OCR FIXES
# --------------------------------------------------

def fix_common_errors(line):

    for wrong, correct in OCR_FIXES.items():

        line = line.replace(
            wrong,
            correct
        )


    return line



# --------------------------------------------------
# REMOVE BAD OCR CHARACTERS
# --------------------------------------------------

def clean_symbols(line):

    # Remove strange repeated characters

    line = re.sub(
        r"[^\x00-\x7F]+",
        "",
        line
    )


    # Remove excessive spaces

    line = re.sub(
        r"\s{3,}",
        " ",
        line
    )


    return line



# --------------------------------------------------
# MAIN CLEAN FUNCTION
# --------------------------------------------------

def clean_ocr(text):

    lines = text.split("\n")


    cleaned = []


    for line in lines:

        line = line.strip()



        if not line:
            continue



        # Remove UI lines

        skip = False


        for pattern in IGNORE_PATTERNS:

            if re.search(
                pattern,
                line,
                re.IGNORECASE
            ):

                skip = True
                break



        if skip:
            continue



        # Fix OCR mistakes

        line = fix_common_errors(
            line
        )



        # Clean symbols

        line = clean_symbols(
            line
        )



        if line:

            cleaned.append(
                line
            )



    return "\n".join(cleaned)