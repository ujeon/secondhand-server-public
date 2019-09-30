from authlib.jose import jwt
from .models import User

import os
import time
import json

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

secret_file = os.path.join(BASE_DIR, "secret.json")


with open(secret_file) as f:
    secret = json.loads(f.read())


def get_secret(setting, secret=secret):
    try:
        return secret[setting]
    except:
        error_msg = "Set key '{0}' in secret.json".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_JWT = get_secret("SECRET_JWT")


def token_generator(property, value):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "iss": "jellyfish",
        "exp": 1500000,
        "iat": int(round(time.time() * 1000)),
    }
    payload[property] = value
    token = jwt.encode(header, payload, SECRET_JWT)
    return token


def decode_token(token):
    claims = jwt.decode(token, SECRET_JWT)
    return claims
