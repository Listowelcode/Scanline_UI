import os
import re

from services.project_metadata import create_metadata



def create_project_folder(name):

    os.makedirs(
        name,
        exist_ok=True
    )

    return name




def extract_language(text):

    match = re.search(
        r"LANGUAGE:\s*(\w+)",
        text,
        re.IGNORECASE
    )


    if match:

        return match.group(1).lower()


    return "unknown"




def extract_code(text):

    match = re.search(
        r"CODE:\s*(.*)",
        text,
        re.DOTALL | re.IGNORECASE
    )


    if match:

        code = match.group(1)


    else:

        code = text



    code = re.sub(
        r"```[a-zA-Z]*",
        "",
        code
    )


    code = code.replace(
        "```",
        ""
    )


    return code.strip()





def get_filename(language):


    files = {

        "python":
            "main.py",

        "javascript":
            "script.js",

        "typescript":
            "script.ts",

        "html":
            "index.html",

        "css":
            "style.css",

        "java":
            "Main.java",

        "cpp":
            "main.cpp",

        "c++":
            "main.cpp",

        "csharp":
            "Program.cs",

        "php":
            "index.php",

        "sql":
            "database.sql"

    }


    return files.get(
        language,
        "code.txt"
    )





def generate_project(ai_output, scan_folder):


    print(
        "Analyzing project structure..."
    )



    # Create project folder inside scan session

    project_folder = os.path.join(
        scan_folder,
        "generated_project"
    )


    folder = create_project_folder(
        project_folder
    )



    language = extract_language(
        ai_output
    )


    print(
        "Detected:",
        language
    )



    code = extract_code(
        ai_output
    )



    filename = get_filename(
        language
    )



    path = os.path.join(
        folder,
        filename
    )



    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            code
        )



    create_metadata(
        folder=folder,

        language=language,

        filename=filename

    )



    print(
        "Created:",
        path
    )



    return folder