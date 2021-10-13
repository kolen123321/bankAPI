from rest_framework import serializers
from accounts.backends import authenticate

from accounts.models import User

from django.contrib.auth.hashers import make_password


class AuthUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16, required=False)
    email = serializers.EmailField(max_length=254, required=True)
    verification = serializers.CharField(max_length=16, required=False)
    password = serializers.CharField(max_length=256, required=True)
    is_staff = serializers.BooleanField(default=False)
    uuid = serializers.CharField(max_length=64, default=None)

    def create(self, validated_data):
        return User.objects.create(email=validated_data['email'], password=validated_data['password'])

class UserSerializer(serializers.ModelSerializer):

    token = serializers.CharField(max_length=256)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        return User.objects.create(email=validated_data['email'], password=make_password(validated_data['password']))
