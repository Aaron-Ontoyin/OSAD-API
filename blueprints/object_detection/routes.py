from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, current_user

from utils import db

from .utils import detect_object
from .models import Image


@jwt_required()
def detect_image():
    """
    Detect the object in the image
    """
    image = request.files.get("image")

    if not image:
        return jsonify({"msg": "No image provided"}), 400

    if image.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        return jsonify({"msg": "Invalid image format. Provide a .jp(e)g or .png"}), 400


    results, file_path = detect_object(image, current_user.id)

    return jsonify(detected_objs=results, img_url=file_path), 200


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
    image = (
        db.session.query(Image).filter_by(id=image_id, user_id=current_user.id).first()
    )
    if not image:
        return jsonify({"msg": "Image not found"}), 404

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
    image = (
        db.session.query(Image).filter_by(id=image_id, user_id=current_user.id).first()
    )
    if not image:
        return jsonify({"msg": "Image not found"}), 404
    db.session.delete(image)
    db.session.commit()
    return make_response("", 204)
