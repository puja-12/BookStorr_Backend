from rest_framework import serializers
from .models import Book
from user.models import User


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'quantity']
