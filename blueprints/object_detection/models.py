import os
from utils import db


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    detected_as = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    url = db.Column(db.String(250), nullable=True)
    detected_on = db.Column(
        db.DateTime, nullable=True, default=db.func.current_timestamp()
    )
