import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


MODEL="tencent/hy3:free"



def clean_code(ocr_text):


    print("Preparing OCR...")


    # Prevent oversized AI requests
    if len(ocr_text) > 12000:

        print(
            "OCR too large. Trimming input..."
        )

        ocr_text = ocr_text[:12000]



    prompt = f"""
You are an expert software engineer who repairs
programming code extracted from tutorial videos.
You are extracting code from a programming tutorial video.

The OCR comes from screenshots, so it may contain:
- VS Code autocomplete suggestions
- unrelated files
- browser text
- previous examples
- random UI text

Your first task is to identify the MAIN tutorial project.

Rules:
1. Find the dominant programming language.
2. Ignore unrelated languages.
3. Do not combine separate projects.
4. Preserve the original tutorial structure.
5. Only output files that belong to the main project.

The following text was extracted using OCR.

OCR mistakes may include:

- confusing < and >
- missing quotes
- broken indentation
- wrong symbols
- incorrect variable names
- duplicated lines
- VS Code suggestions mixed into code


YOUR TASK:

1. Identify the programming language.

Possible languages:

- HTML
- CSS
- JavaScript
- Python
- Java
- C++
- C#
- PHP
- SQL
- Other


2. Restore the original code.

3. Remove:
- VS Code menus
- autocomplete suggestions
- line numbers
- browser text
- unrelated words


4. Do NOT redesign the project.

5. Do NOT add features.

6. Only repair what OCR damaged.

You are ScanLine OCR extraction engine.

Your ONLY job is to recover the EXACT code visible in the video frames.

DO NOT:
- rewrite code
- improve code
- create your own solution
- guess missing code
- generate examples
- complete unfinished programs

If OCR is unclear:
- keep the closest visible text
- do not invent replacements

Remove only:
- random UI text
- editor menus
- browser text
- unrelated examples

The final code must match what appeared on screen.

If multiple languages exist:

Separate them clearly.

OCR TEXT:

{ocr_text}

"""


    print(
        "Sending OCR to AI..."
    )



    try:


        response = client.chat.completions.create(

            model=MODEL,


            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],


            temperature=0.1

        )



        # Debug response if AI fails

        if response.choices is None:


            print(
                "AI ERROR RESPONSE:"
            )

            print(response)


            return """

LANGUAGE:
unknown


CODE:

AI failed to return code.

"""



        result = response.choices[0].message.content



        print(
            "AI cleanup complete!"
        )


        return result



    except Exception as e:


        print(
            "AI request failed:"
        )


        print(e)



        return """

LANGUAGE:
unknown


CODE:

AI request failed.

"""