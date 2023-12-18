import os
import shutil
from uuid import uuid4
import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment

from settings import Config
from .models import AudioText
from utils import db


base_url = Config.BASE_URL
audio_folder = os.path.join(
    base_url, "blueprints", "text_audio_processing", "static", "audio"
)
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)


def audio_processer(audio, user_id):
    """
    Process the audio and produce its text equivalent
    Args:
        audio: url of the audio
        user_id: id of the user
    Returns:
        (audio, text) db objects
    """
    audio.save("temp_audio_file")
    audio_format = audio.filename.split(".")[-1]
    if audio_format not in ["wav", "aiff", "flac"]:
        # change audio format to wav
        audio = AudioSegment.from_file("temp_audio_file", format=audio_format)
        with open("temp_audio_file", "wb") as f:
            audio.export(f, format="wav")
        audio_format = "wav"

    with open("temp_audio_file", "rb") as audio:
        # Convert audio to text
        r = sr.Recognizer()
        with sr.AudioFile(audio) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)

        # Save audio
        audio.seek(0)
        audio_save_to_path = os.path.join(audio_folder, str(uuid4()) + "." + audio_format)
        with open(audio_save_to_path, "wb") as f:
            shutil.copyfileobj(audio, f)

    save_audio_and_text(text, audio_save_to_path, user_id)

    os.remove("temp_audio_file")
    return text, audio_save_to_path


def text_processer(text, user_id):
    """
    Process the text and produce its audio equivalent
    Args:
        text: text to be processed
        user_id: id of the user
    Returns:
        (audio, text) db objects
    """

    audio_full_path = os.path.join(audio_folder, str(uuid4()) + ".mp3")
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_full_path)
    engine.runAndWait()

    # Store audio in the database
    save_audio_and_text(text, audio_full_path, user_id)

    return audio_full_path, text


def save_audio_and_text(text, audio_path, user_id):
    """
    Save the audio and text in the database
    Args:
        text: text to be saved
        audio_path: path of the audio
        user_id: id of the user
    """

    audio_text = AudioText(text_value=text, audio_url=audio_path, user_id=user_id)
    db.session.add(audio_text)
    db.session.commit()

    return
