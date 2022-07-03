"""
Title:      utils.py
Desc:       contains user utility functions for the user model
"""
import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _unused, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path,
                                'static/profile_pics',
                                picture_filename, )

    # resize an uploaded picture using the Pillow module
    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_filename


