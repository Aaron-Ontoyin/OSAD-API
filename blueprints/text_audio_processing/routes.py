from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, current_user

from utils import db
from .utils import audio_processer, text_processer
from .models import AudioText


@jwt_required()
def process_text():
    """
    Process the text and produce its audio equivalent
    """
    text = request.json.get("text")
    audio_url, text_value = text_processer(text, current_user.id)

    return jsonify(text=text_value, audio_url=audio_url), 200


@jwt_required()
def process_audio():
    """
    Process the audio and produce its text equivalent
    """
    audio = request.files.get("audio")
    audio_format = audio.filename.split(".")[-1]

    if audio_format not in ["wav", "aiff", "flac", "mp3", "m4a"]:
        return jsonify(error="Unsupported audio format"), 400

    text_value, audio_url = audio_processer(audio, current_user.id)

    return jsonify(text=text_value, audio_url=audio_url), 200


@jwt_required()
def get_audio_text():
    """
    Get the text and audio details from the database
    """
    audio_text_id = request.json.get("audio_text_id")
    audio_text = (
        db.session.query(AudioText)
        .filter_by(id=audio_text_id, user_id=current_user.id)
        .first()
    )
    if not audio_text:
        return jsonify(msg="Audio text not found"), 404

    response = jsonify(
        {
            "id": audio_text.id,
            "text": audio_text.text_value,
            "audio_url": audio_text.audio_url,
            "processed_on": audio_text.processed_on,
        }
    )

    return response, 200


@jwt_required()
def get_all_audio_texts():
    """
    Get all the text and audio details from the database
    """
    all_audio_texts = AudioText.query.filter_by(user_id=current_user.id).all()
    audio_text_list = [
        {
            "id": audio_text.id,
            "text": audio_text.text_value,
            "audio_url": audio_text.audio_url,
            "processed_on": audio_text.processed_on,
        }
        for audio_text in all_audio_texts
    ]
    return jsonify(audio_text_list), 200


@jwt_required()
def delete_audio_text():
    """
    Delete the text and audio details from the database
    """
    audio_text_id = request.json.get("audio_text_id")
    audio_text = db.session.query(AudioText).filter_by(
        id=audio_text_id, user_id=current_user.id
    ).first()
    if not audio_text:
        return jsonify(msg="Audio Text not found"), 404
    db.session.delete(audio_text)
    db.session.commit()
    return make_response("", 204)
