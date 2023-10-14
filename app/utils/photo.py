import os
import base64
import io
import uuid
from PIL import Image
from fastapi import HTTPException


def from_base_to_photo(code: str, path_folder: str):
    path = f'{path_folder}/{str(uuid.uuid4())}.webp'
    binary_data = base64.b64decode(code)
    image = Image.open(io.BytesIO(binary_data))
    image.save(path, 'webp')
    return path


def from_photo_to_base(path: str):
    with open(path, "rb") as image_file:
        image_binary_data = image_file.read()
    base64_encoded_image = base64.b64encode(image_binary_data).decode("utf-8")
    return base64_encoded_image


def delete_photo(path: str):
    try:
        os.remove(path)
    except Exception as e:
        raise HTTPException(500, "Error when delete photo " + str(e))
