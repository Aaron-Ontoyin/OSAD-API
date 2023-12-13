from flask import Blueprint

from .routes import process_audio, process_text


text_audio_processing = Blueprint("text_audio_processing", __name__, static_folder="static")


text_audio_processing.post("/process-text")(process_text)
text_audio_processing.post("/process-audio")(process_audio)
