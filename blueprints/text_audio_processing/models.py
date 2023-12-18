from utils import db


class AudioText(db.Model):
    __tablename__ = "audio_text"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    audio_url = db.Column(db.String(250), nullable=True)
    text_value = db.Column(db.String(2000), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    processed_on = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
