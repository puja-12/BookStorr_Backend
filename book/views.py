import logging
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from book.serializers import BookListSerializer
from user.utils import get_respone, verify_superuser
from .models import Book
from book.utils import  RedisBook


logger = logging.getLogger()


class GetAllBookListView(APIView):
    """
    Class view for getting all the book
    """

    def get(self, request):
        """
        get function for requesting get method to get all the book
        """
        try:

            book_list = Book.objects.all()
            serializer = BookListSerializer(book_list, many=True)

            return get_respone(message="All Book", data=serializer.data, status=200)
        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went Wrong",
                               status=400)

    @verify_superuser
    def delete(self, request):
        """
        get function for requesting delete method to delete the book
        """
        try:
            book = Book.objects.get(id=request.data.get("id"))
            book.delete()

            return get_respone(message="delete successfully", status=204)
        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went Wrong", status=400)

    @verify_superuser
    def put(self, request):
        """
        get function for requesting put method to update all the book
        """
        try:
            book = Book.objects.get(id=request.data.get("id"))
            serializers = BookListSerializer(instance=book, data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()

            return get_respone(message="book updated successfully", data=serializers.data, status=200)
        except ValidationError as e:
            return get_respone(message=e.detail, status=400)
        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went Wrong", status=400)

    @verify_superuser
    def post(self, request):
        """
        get function for requesting post method to create book
        """
        try:

            serializers = BookListSerializer(data=request.data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return get_respone(message="book added successfully", data=serializers.data, status=201)
        except ValidationError as e:
            return get_respone(message=e.detail, status=204)
        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went Wrong", status=400)
