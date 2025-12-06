import os


def path(file_name):
    current_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(current_dir, file_name)

