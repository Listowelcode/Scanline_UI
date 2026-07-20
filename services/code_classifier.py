import re


def classify_code(text):

    text = text.lower()


    scores = {
        "html": 0,
        "css": 0,
        "javascript": 0,
        "python": 0,
        "sql": 0
    }


    # HTML indicators
    html_patterns = [
        "<html",
        "<body",
        "<div",
        "<form",
        "<input",
        "<button",
        "doctype",
        "class="
    ]


    # CSS indicators
    css_patterns = [
        "{",
        "}",
        "margin:",
        "padding:",
        "color:",
        "background:",
        "display:",
        "font-size:"
    ]


    # Javascript indicators
    js_patterns = [
        "function",
        "const ",
        "let ",
        "var ",
        "document.",
        "queryselector",
        "onclick",
        "addEventListener"
    ]


    # Python indicators
    python_patterns = [
        "def ",
        "import ",
        "print(",
        "class ",
        "__init__"
    ]


    # SQL indicators
    sql_patterns = [
        "select ",
        "insert ",
        "update ",
        "delete ",
        "create table",
        "from "
    ]



    for item in html_patterns:
        if item in text:
            scores["html"] += 1


    for item in css_patterns:
        if item in text:
            scores["css"] += 1


    for item in js_patterns:
        if item in text:
            scores["javascript"] += 1


    for item in python_patterns:
        if item in text:
            scores["python"] += 1


    for item in sql_patterns:
        if item in text:
            scores["sql"] += 1



    result = max(
        scores,
        key=scores.get
    )


    # if no clues found
    if scores[result] == 0:
        return "unknown"


    return result