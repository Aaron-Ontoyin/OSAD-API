import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify
from blueprints import auth, object_detection, text_audio_processing

from utils import db, bcrypt, jwt

app = Flask(__name__)

load_dotenv()

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))) or timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES'))) or timedelta(days=30)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

jwt.init_app(app)
bcrypt.init_app(app)
db.init_app(app)
with app.app_context():
    # TODO: Create default admin
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
    app.run(debug=True)
