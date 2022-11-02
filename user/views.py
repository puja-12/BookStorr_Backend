import json
import logging

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError

from user.serializers import RegisterSerializer
from user.utils import get_respone

logger = logging.getLogger('django')


@api_view(['POST'])
def register_api(request):
    """
    post method for registering a user
    """
    try:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("User successfully Registered ")
        return get_respone(data=serializer.data, message='Register successfully', status=201)
    except ValidationError as e:
        logger.exception(e)
        return get_respone(message=e.detail, status=400)
    except Exception as e:
        logger.exception(e)
        return get_respone(message=str(e), status=400)


@api_view(['POST'])
def log_in(request):
    """
     post method for checking login operation
    """
    try:
        user = authenticate(**request.data)
        if user:
            logger.info("User is successfully logged in")
            # return Response({'success': True, 'message': 'Login Success'})
            return get_respone(message='Login success')

        return get_respone(message='Invalid credentials used!',status=401)

    except Exception as e:
        logger.exception(e)
        return get_respone(message= 'Login failed!, Something Went Wrong',
                             data=str(e),status=400)
