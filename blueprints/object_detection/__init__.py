from flask import Blueprint

from .routes import detect_image


object_detection = Blueprint("object_detection", __name__, static_folder="static")

object_detection.post("/detect-image")(detect_image)
