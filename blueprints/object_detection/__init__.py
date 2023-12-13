from flask import Blueprint

from .routes import detect_image, get_image, get_images, delete_image


object_detection = Blueprint("object_detection", __name__, static_folder="static")

object_detection.post("/detect-image")(detect_image)
object_detection.get("/get-image")(get_image)
object_detection.get("/get-images")(get_images)
object_detection.delete("/delete-image")(delete_image)
