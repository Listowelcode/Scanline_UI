import os
import zipfile
import re



def clean_filename(title):

    # Remove unsafe filename characters
    # Also removes # because it breaks URLs

    title = re.sub(
        r'[^\w\s-]',
        "",
        title
    )


    # Replace spaces with underscores

    title = title.replace(
        " ",
        "_"
    )


    # Remove multiple underscores

    title = re.sub(
        r'_+',
        '_',
        title
    )


    # Limit filename length

    title = title[:100]


    return title.strip("_")





def create_zip(folder, title, scan_folder):


    safe_title = clean_filename(
        title
    )


    zip_name = os.path.join(
        scan_folder,
        f"{safe_title}.zip"
    )



    with zipfile.ZipFile(
        zip_name,
        "w"
    ) as zipf:


        for root, dirs, files in os.walk(folder):


            for file in files:


                filepath = os.path.join(
                    root,
                    file
                )


                zipf.write(

                    filepath,

                    os.path.relpath(
                        filepath,
                        folder
                    )

                )



    return zip_name