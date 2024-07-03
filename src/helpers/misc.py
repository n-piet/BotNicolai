import os


def file_exists(file_path):
    return os.path.exists(file_path)


def check_if_file_exists(
    file_path,
    target_func,
    *args,
):
    if not file_exists(file_path):
        target_func(*args)
    else:
        print(f"The file {file_path} already exists")
