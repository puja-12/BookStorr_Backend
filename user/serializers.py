from rest_framework import serializers
from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'full_name','first_name','last_name', 'email', 'password', 'mobile']
        extra_kwargs = {
            'password': {'write_only': True,},
            'first_name': {'write_only': True, },
            'last_name': {'write_only': True, },
            'full_name': {'read_only': True, },
        }

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)