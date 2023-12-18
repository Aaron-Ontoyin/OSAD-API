from flask import Flask, jsonify
from utils import db, bcrypt, jwt
from blueprints import auth, object_detection, text_audio_processing
from settings import config

app = Flask(__name__)
app.config.from_object(config['development'])

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(object_detection, url_prefix='/object-detection')
app.register_blueprint(text_audio_processing, url_prefix='/tap')


@app.get('/')
def root():
    """
    This function is the root endpoint of the API.

    Returns:
        dict: A JSON response containing a welcome message.
    """
    return jsonify({"message": "Welcome to OSAD API!"})


if __name__ == '__main__':
    app.run()
