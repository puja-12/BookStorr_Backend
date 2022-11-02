from rest_framework.response import Response


def get_respone(data={},message="",status=200):
    return Response({'message': message, 'data': data}, status=status)