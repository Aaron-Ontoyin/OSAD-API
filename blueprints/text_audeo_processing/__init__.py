from flask import Blueprint

from .routes import process_audio, process_text


text_audio_processing = Blueprint("text_audio_processing", __name__, static_folder="static")


text_audio_processing.post("/get-text")(process_text)
text_audio_processing.post("/get-audio")(process_audio)
