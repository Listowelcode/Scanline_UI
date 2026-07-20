progress = {
    "progress": 0,
    "message": "Waiting...",
    "file": None,
    "status": "idle"
}


def update_progress(value, message, file=None):

    progress["progress"] = value
    progress["message"] = message

    if file:
        progress["file"] = file



def set_status(status):

    progress["status"] = status



def get_progress():

    return progress