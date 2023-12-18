from flask import Blueprint

from .routes import process_audio, process_text, get_audio_text, get_all_audio_texts, delete_audio_text


text_audio_processing = Blueprint("text_audio_processing", __name__, static_folder="static")


text_audio_processing.post("/process-text")(process_text)
text_audio_processing.post("/process-audio")(process_audio)
text_audio_processing.get("/get-audio-text")(get_audio_text)
text_audio_processing.get("/get-all-audio-texts")(get_all_audio_texts)
text_audio_processing.delete("/delete-audio-text")(delete_audio_text)
