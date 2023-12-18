import os
from dotenv import load_dotenv

load_dotenv()

# ----------------------------- POSTGRES DB ---------------------------------#
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ------------------------------- REDIS DB -----------------------------------#
import redis

rurl = os.getenv("REDIS_URL")
rhost = rurl.split(":")[1].strip("//")
rport = rurl.split(":")[2].split("/")[0]
rdb = rurl.split(":")[2].split("/")[1]
redis_client = redis.StrictRedis(host=rhost, port=rport, db=rdb, decode_responses=True)


# -------------------------------- JWT ---------------------------------------#
from flask_jwt_extended import JWTManager

jwt = JWTManager()


# -------------------------------- BCRYPT -------------------------------------#
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


# -------------------------------- EMAIL --------------------------------------#
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

smtp = smtplib.SMTP("smtp.gmail.com", 587)
context = ssl.create_default_context()
smtp.ehlo()
smtp.starttls(context=context)

email_password = os.getenv("SMTP_EMAIL_PASSWORD")
email_address = os.getenv("SMTP_EMAIL_ADDRESS")

def send_mail(to=None, title=None, msg="", img=None, attachment=None):
    """
    Sends an email using the Gmail SMTP server.

    Args:
        to (str): The email address of the recipient.
        title (str): The subject line of the email.
        msg (str): The body of the email.
        img (str): The path to an image file to attach to the email.
        attachment (str): The path to a file to attach to the email.

    Returns:
        None
    """

    smtp.login(email_address, email_password)

    msg = create_email_message(subject=title, text=msg, img=img, attachment=attachment)
    smtp.sendmail(from_addr=email_address, to_addrs=[to,], msg=msg.as_string())

    smtp.quit()


def create_email_message(subject="", text="", img=None, attachment=None):
    """
    Create a MIME multipart message with the given subject, text, image(s), and attachment(s).

    Args:
        subject (str): The subject of the email message.
        text (str): The body text of the email message.
        img (str or list of str): The path(s) to the image(s) to attach to the email message.
        attachment (str or list of str): The path(s) to the file(s) to attach to the email message.

    Returns:
        MIMEMultipart: The MIME multipart message object with the specified components.
    """

    msg = MIMEMultipart()

    msg["Subject"] = subject

    msg.attach(MIMEText(text))

    if img is not None:
        if type(img) is not list:
            img = [img]

        for one_img in img:
            img_data = open(one_img, "rb").read()
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))

    if attachment is not None:
        if type(attachment) is not list:
            attachment = [attachment]

        for one_attachment in attachment:
            with open(one_attachment, "rb") as f:
                file = MIMEApplication(f.read(), name=os.path.basename(one_attachment))

            file[
                "Content-Disposition"
            ] = f'attachment; filename="{os.path.basename(one_attachment)}"'

            msg.attach(file)

    return msg
