import os

from settings import Config
from utils import db
from .models import Image


def detect_object(image):
    """
    Detect the object in the image
    """
    # TODO: Implement object detection logic

    response_data = {
        "label": "Object is a beast!",
        "description": "Looking at the image, you can see that the object is a beast!",
    }
    return response_data


def store_image_in_database(image, detected_as, description, user_id):
    """
    Store the image in the database
    """
    base_url = Config.BASE_URL
    upload_folder = os.path.join(
        base_url, "bluesprints", "object_detection", "static", "images"
    )
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, image.filename)
    image_db_obj = Image(
        user_id=user_id,
        detected_as=detected_as,
        description=description,
        url=file_path,
        detected_on=db.func.current_timestamp(),
    )
    image.save(file_path)
    db.session.add(image_db_obj)
    db.session.commit()

    return
