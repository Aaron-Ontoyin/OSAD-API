import os
import warnings
from uuid import uuid4

import torch
from torchvision.models.detection import (
    fasterrcnn_resnet50_fpn_v2,
    FasterRCNN_ResNet50_FPN_V2_Weights,
)
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image
from torchvision import transforms as T

from PIL import Image as PILImage

from settings import Config
from utils import db
from .models import Image as DBModelImage


weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
model = fasterrcnn_resnet50_fpn_v2(box_score_thresh=0.9, weights=weights)
model.eval()
cuda = torch.cuda.is_available()
if cuda:
    model.cuda()
    weights.cuda()
preprocess = weights.transforms()


def detect_object(image, user_id):
    """
    Detect the object in the image
    """
    img_extension = image.filename.split(".")[-1]
    img = PILImage.open(image).convert("RGB")
    img = T.ToTensor()(img)
    batch = [preprocess(img)]

    predictions = model(batch)[0]
    labels = [weights.meta["categories"][i] for i in predictions["labels"]]
    num_detected = len(labels)

    img_uint8 = (img * 255).byte()
    with warnings.catch_warnings():
        # Ignore warnings that contain "boxes doesn't contain any box. No box was drawn" in their message
        warnings.filterwarnings("ignore", category=UserWarning, message=".*boxes doesn't contain any box. No box was drawn.*")
        box = draw_bounding_boxes(
            img_uint8,
            boxes=predictions["boxes"],
            labels=labels,
            colors="blue",
            width=4,
            font="arial",
            font_size=30,
        )
    img = to_pil_image(box.detach())

    results = {
        "detected_as": labels,
        "description": f"{num_detected} object(s) detected in the image",
    }

    file_path = store_image_in_database(
        image=img,
        img_extension=img_extension,
        user_id=user_id,
        detected_as=labels,
        description=results["description"],
    )

    return results, file_path


def store_image_in_database(image, img_extension, detected_as, description, user_id):
    """
    Store the image in the database
    Args:
        image: PIL Image
        img_extension: string
        detected_as: list
        description: string
        user_id: integer
    Returns:
        file_path: string
    """
    base_url = Config.BASE_URL
    upload_folder = os.path.join(
        base_url, "blueprints", "object_detection", "static", "images"
    )
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(
        upload_folder, str(uuid4()) + "." + img_extension
    )
    image.save(file_path)
    image_db_obj = DBModelImage(
        user_id=user_id,
        detected_as=detected_as,
        description=description,
        url=file_path,
        detected_on=db.func.current_timestamp(),
    )
    db.session.add(image_db_obj)
    db.session.commit()

    return file_path
