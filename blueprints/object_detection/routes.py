from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from utils import db

from .utils import detect_object, store_image_in_database
from .models import Image


@jwt_required()
def detect_image():
    """
    Detect the object in the image
    """
    image = request.files.get("image")
    if not image:
        return jsonify({"msg": "No image provided"}), 400
    results = detect_object(image)
    store_image_in_database(
        image=image,
        detected_as=results["label"],
        description=results["description"],
        user_id=current_user.id,
    )
    return jsonify(results), 200


@jwt_required()
def get_images():
    """
    Get all the images of this user
    """
    all_images = Image.query.filter_by(user_id=current_user.id).all()
    image_list = [
        {
            "id": image.id,
            "url": image.url,
            "detected_as": image.detected_as,
            "detected_on": image.detected_on,
            "description": image.description,
            "user_id": image.user_id,
        }
        for image in all_images
    ]
    return jsonify(image_list), 200


@jwt_required()
def get_image():
    """
    Get the image of this user
    """
    image_id = request.json.get("image_id")
    image = db.session.get(Image, image_id)
    return (
        jsonify(
            {
                "id": image.id,
                "detected_as": image.detected_as,
                "description": image.description,
                "url": image.url,
                "detected_on": image.detected_on,
                "user_id": image.user_id,
            }
        ),
        200,
    )


@jwt_required()
def delete_image():
    """
    Delete the image of this user
    """
    image_id = request.json.get("image_id")
    image = db.session.get(Image, image_id)
    if not image:
        return jsonify({"msg": "Image not found"}), 404
    db.session.delete(image)
    db.session.commit()
    return jsonify({"msg": "Image deleted successfully"}), 204
