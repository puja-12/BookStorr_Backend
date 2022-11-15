import logging
from datetime import datetime, timedelta

from django.contrib.auth import authenticate
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from user.models import User
from user.serializers import RegisterSerializer
from user.token import Jwt
from user.utils import get_respone, Email

logger = logging.getLogger('django')


class UserRegistration(APIView):

    def post(self, request):

        """
        post method for registering a user
        """
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            Email.verify_user(id=serializer.data.get('id'), username=serializer.data.get('username'),
                              email=serializer.data.get('email'))
            logger.info("User successfully Registered ")
            return get_respone(data=serializer.data, message='Register successfully,Please verified your Email',
                               status=201)
        except ValidationError as e:
            logger.exception(e)
            return get_respone(message=e.detail, status=400)
        except Exception as e:
            logger.exception(e)
            return get_respone(message=str(e), status=400)


class UserLogin(APIView):

    def post(self, request):
        """
         post method for checking login operation
        """
        try:
            user = authenticate(**request.data)
            if user:
                if user.is_verify:
                    token = Jwt.encode_token(
                        payload={'user_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=60)})
                    return get_respone(message='Login success', data={'token': token})
                Email.verify_user(user.id, user.username, user.email)
                return get_respone(message=' user is not verified and check email', status=401)
            return get_respone(message='Invalid credentials used!', status=401)
        except Exception as e:
            logger.exception(e)
            return get_respone(message=str(e), status=400)


class VarifyUser(APIView):
    """
    Validating the token if the user is valid or not
    """

    def get(self, request, token):
        try:
            decode_token = Jwt.decode_token(token=token)
            user = User.objects.get(username=decode_token.get('username'))
            user.is_verify = True
            user.save()
            return get_respone(message="User verified", status=201)
        except Exception as e:
            logging.error(e)
            return get_respone(data=str(e), status=400)
