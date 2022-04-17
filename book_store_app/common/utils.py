import base64
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
from functools import wraps

import jwt
import os

from flask import request

password = os.getenv("password")
my_email = os.getenv("my_email")


def generate_token(otp, user_id):
    token = jwt.encode(
        {'otp': otp, 'user_id': user_id, 'Exp': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=60000000))},
        str(os.environ.get('SECRET_KEY')))
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access-token' in request.headers:
            short_token = request.headers.get('access-token')
        else:
            short_token = request.args.get('token')
        token = get_real_token(short_token)
        if not token:
            return {'Message': 'Token is missing!', 'code': 409}
        try:
            data = jwt.decode(token, str(os.environ.get('SECRET_KEY')), algorithms=["HS256"])
        except Exception as e:
            return {'Error': str(e), 'code': 409}

        return f(data['otp'], data['user_id'])

    return decorated


def get_short_token(token):
    token_string_bytes = token.encode("ascii")

    base64_bytes = base64.b64encode(token_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def get_real_token(token_):
    base64_bytes = token_.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")

    return sample_string


def send_mail(email, message):
    msg = MIMEMultipart()

    passwrd = password
    msg['From'] = my_email
    msg['To'] = email
    msg['Subject'] = "Click on the link"

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    server.login(msg['From'], passwrd)

    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()


def generate_otp():
    otp = random.randint(1000, 9999)
    return otp
