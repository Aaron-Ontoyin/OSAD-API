import os

from flask_jwt_extended import current_user

from utils import db
from .models import Image


def detect_object(image):
    """
    Detect the object in the image
    """
    # TODO: Implement object detection logic

    response_data = {
        "result": "Object is a beast!",
        "description": "Looking at the image, you can see that the object is a beast!",
    }
    return response_data


def store_image_in_database(image):
    """
    Store the image in the database
    """
    upload_folder = os.path.join(os.path.dirname(__file__), 'static/images')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, image.filename)
    image_db_obj = Image(
        user_id=current_user.id,
        detected_as="beast",
        description="Looking at the image, you can see that the object is a beast!",
        path=file_path,
        detected_on=db.func.current_timestamp(),
    )
    image.save(file_path)
    db.session.add(image_db_obj)
    db.session.commit()

    return
