from flask import request, jsonify
from flask_jwt_extended import jwt_required

from .utils import detect_object, store_image_in_database


@jwt_required()
def detect_image():
    """
    Detect the object in the image
    """
    image = request.files.get('image')
    if not image:
        return jsonify({"message": "No image provided"}), 400
    results = detect_object(image)
    store_image_in_database(image)
    return jsonify(results), 200


@jwt_required()
def get_images():
    """
    Get all the images of this user
    """
    # TODO: Implement logic
    return jsonify({"message": "Not implemented yet"}), 200


@jwt_required()
def get_image(image_id):
    """
    Get the image of this user
    """
    # TODO: Implement logic
    return jsonify({"message": "Not implemented yet"}), 200


@jwt_required()
def delete_image(image_id):
    """
    Delete the image of this user
    """
    # TODO: Implement logic
    return jsonify({"message": "Not implemented yet"}), 200