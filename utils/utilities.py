import os
from dotenv import load_dotenv

load_dotenv()

#----------------------------- POSTGRES DB ---------------------------------#
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#------------------------------- REDIS DB -----------------------------------#
import redis

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0, decode_responses=True
)


#-------------------------------- JWT ---------------------------------------#
from flask_jwt_extended import JWTManager

jwt = JWTManager()


#-------------------------------- BCRYPT -------------------------------------#
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


#-------------------------------- EMAIL --------------------------------------#
def send_email(recipient, subject, message):
    """
    Sends an email to the recipient with the subject and message
    """
    # TODO: Implement logic
    with open("reset_password_token.txt", "w") as f:
        f.write(message)

    return
