import os


def allowed_file(filename, allowed_extensions):

    # Check extension exists
    if "." not in filename:
        return False

    # Extract extension
    extension = filename.rsplit(".", 1)[1].lower()

    return extension in allowed_extensions