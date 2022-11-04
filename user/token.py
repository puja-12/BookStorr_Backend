import logging

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


class Jwt:
    @staticmethod
    def encode_token(payload):
        """
        encoding after checking if instance is dictionary using jwt encode

        """
        try:
            if payload.get('exp') is None:
                payload.update({"exp": settings.JWT_EXPIRING_TIME})

            return jwt.encode(payload, settings.JWT_SECRET_KEY,
                                       algorithm="HS256")

        except Exception as e:
            logging.exception(e)
            return None

    @staticmethod
    def decode_token(token):
        """
      decoding the token aftre getting the encoded token usind decode method

        """
        return  jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])