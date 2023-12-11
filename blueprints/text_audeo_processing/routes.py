from flask import request, jsonify
from flask_jwt_extended import jwt_required

from .utils import audio_processer, text_processer


@jwt_required()
def process_text():
    """
    Process the text and produce its audio equivalent
    """
    text = request.form.get("text")
    results = text_processer(text)

    return jsonify(results), 200


@jwt_required()
def process_audio():
    """
    Process the audio and produce its text equivalent
    """
    audio = request.form.get("audio")
    results = audio_processer(audio)

    return jsonify(results), 200

