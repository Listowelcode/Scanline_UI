import re
import os



EXTENSIONS = {

    ".html": "html",
    ".htm": "html",

    ".css": "css",

    ".js": "javascript",
    ".jsx": "javascript",

    ".ts": "typescript",
    ".tsx": "typescript",

    ".py": "python",

    ".java": "java",

    ".cpp": "cpp",
    ".c": "cpp",

    ".cs": "csharp",

    ".php": "php",

    ".sql": "sql"

}





FILE_PATTERNS = {


    "html": [
        r"<!DOCTYPE\s+html>",
        r"<html",
        r"<body",
        r"<div"
    ],


    "css": [
        r"\w+\s*\{",
        r"margin\s*:",
        r"padding\s*:",
        r"color\s*:"
    ],


    "javascript": [
        r"function\s+",
        r"const\s+",
        r"let\s+",
        r"document\.",
        r"addEventListener"
    ],


    "typescript": [
        r"interface\s+\w+",
        r"type\s+\w+\s="
    ],


    "python": [
        r"def\s+\w+\(",
        r"import\s+",
        r"from\s+\w+\s+import",
        r"print\("
    ],


    "java": [
        r"public\s+class",
        r"System\.out\.println"
    ],


    "cpp": [
        r"#include",
        r"cout\s*<<"
    ],


    "csharp": [
        r"using\s+System",
        r"Console\.WriteLine"
    ],


    "php": [
        r"<\?php",
        r"\$[a-zA-Z_]"
    ],


    "sql": [
        r"SELECT\s+",
        r"CREATE TABLE",
        r"INSERT INTO"
    ]

}





def detect_file_language(filename, code=""):


    detected = []


    # -----------------------
    # Check extension
    # -----------------------

    ext = os.path.splitext(filename)[1]


    if ext in EXTENSIONS:

        detected.append(
            EXTENSIONS[ext]
        )



    # -----------------------
    # Check code content
    # -----------------------

    for language, patterns in FILE_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                code,
                re.IGNORECASE
            ):

                if language not in detected:

                    detected.append(
                        language
                    )

                break



    return detected





def detect_project_structure(files):


    languages = []



    for filename, code in files.items():


        detected = detect_file_language(
            filename,
            code
        )


        languages.extend(
            detected
        )



    if len(languages) == 0:

        languages.append(
            "unknown"
        )



    return {

        "languages": list(set(languages)),

        "count": len(set(languages))

    }