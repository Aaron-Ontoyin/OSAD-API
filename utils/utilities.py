import os
from dotenv import load_dotenv

load_dotenv()

#----------------------------- POSTGRES DB ---------------------------------#
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#------------------------------- REDIS DB -----------------------------------#
import redis

rurl = os.getenv("REDIS_URL")
rhost = rurl.split(":")[1].strip("//")
rport = rurl.split(":")[2].split("/")[0]
rdb = rurl.split(":")[2].split("/")[1]
redis_client = redis.StrictRedis(
    host=rhost, port=rport, db=rdb, decode_responses=True
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
