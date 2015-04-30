import jwt
from os import environ


def decode_token(token):
    return jwt.decode(token, environ.get('JWT_SECRET'))


def encode_token(payload):
    return jwt.encode(payload, environ.get('JWT_SECRET'))
