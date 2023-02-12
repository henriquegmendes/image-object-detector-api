import os

import requests

def create_dir_if_not_exists(path_dir: str):
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

def download_file(file_path: str, url: str, file_name: str) -> str:
    full_path = os.path.sep.join([file_path, file_name])

    create_dir_if_not_exists(file_path)

    response = requests.get(url, stream=True)

    with open(full_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

    return full_path

def delete_file(path: str):
    os.remove(path)