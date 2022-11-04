from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.request import Request
from rest_framework.response import Response

from user.models import User
from user.token import Jwt


def get_respone(data={}, message="", status=200):
    return Response({'message': message, 'data': data}, status=status)


class Email:
    @staticmethod
    def verify_user(id, username, email):
        try:
            mail_subject = "Verification mail"
            token = Jwt.encode_token(payload={'user_id': id,
                                              'username': username

                                              })
            mail_message = "Click on this http://127.0.0.1:8000/user/verify/" + token

            send = send_mail(mail_subject,
                             mail_message,
                             settings.EMAIL_HOST_USER,
                             [email], fail_silently=False)


        except SMTPAuthenticationError as e:
            print(e)
            raise e

        except Exception as e:
            print(e)


def verify_token(function):
    """
    function for checking and verifying token for valid user
    """

    def wrapper(*args, **kwargs):
        request = list(filter(lambda x: isinstance(x, Request), args))[0]

        token = request.headers.get("Token")
        if not token:
            raise Exception("Token is invalid")
        decode = Jwt().decode_token(token=token)
        user_id = decode.get("user_id")
        if not user_id:
            raise Exception("Invalid user")
        try:
            User.objects.get(id=1000)

        except User.DoesNotExist:
            raise Exception(" user not found")

        request.data.update({"user": user_id})
        return function(*args, **kwargs)

    return wrapper
