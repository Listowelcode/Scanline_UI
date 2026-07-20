import re



def split_code(text):

    files = {}


    # Remove markdown wrapper

    blocks = re.findall(
        r"```(\w+)?\s*(.*?)```",
        text,
        re.DOTALL
    )


    for language, code in blocks:


        code = code.strip()


        if not code:
            continue



        language = language.lower()



        if language in ["html", "htm"]:

            files["index.html"] = code



        elif language == "css":

            files["style.css"] = code



        elif language in ["javascript", "js"]:

            files["script.js"] = code



        elif language in ["python", "py"]:

            files["main.py"] = code



        elif language == "java":

            files["Main.java"] = code



        elif language in ["cpp", "c++"]:

            files["main.cpp"] = code



        elif language in ["csharp", "cs"]:

            files["Program.cs"] = code



        elif language == "php":

            files["index.php"] = code



        elif language == "sql":

            files["database.sql"] = code



    return files