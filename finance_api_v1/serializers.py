from rest_framework import serializers
from accounts.backends import authenticate

from accounts.models import User

from .models import *

from connect_api_v1.serializers import UserSerializer

from django.contrib.auth.hashers import make_password


class FinanceProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = FinanceProfile
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        return Transaction.objects.create(from_profile=validated_data['from_profile'], to_profile=validated_data['to_profile'], amount=validated_data['amount'])

class TransactionDepthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        depth = 1


    