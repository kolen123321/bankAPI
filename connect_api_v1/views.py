from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.backends import JWTAuthentication

from .serializers import UserSerializer, AuthUserSerializer

from accounts.models import User

from accounts.backends import authenticate

import random

from django.db import IntegrityError

from finance_api_v1.models import FinanceProfile


class AuthView(APIView):

    serializer = AuthUserSerializer

    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if not user:
            return Response({'success': False, 'message': 'Пользователь не найден'}, status=404)
        return Response(UserSerializer(user).data, status=200)

class RegisterView(APIView):

    serializer = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'access_token': user.token 
        }, status=200)

class VerificateUserView(APIView):

    authentication_classes = [JWTAuthentication]

    def patch(self, request, id):
        if not User.objects.filter(id=id).exists():
            return Response({
                'success': False,
                'message': 'Пользователь не найден'
            })
        if not 'verification' in request.data:
            return Response({
                'success': False,
                'message': 'Введите уровень верефикации'
            })
        user = User.objects.get(id=id)
        user.verification = request.data['verification']
        try:
            if request.data['verification'] != "register":
                if not 'username' in request.data:
                    return Response({
                        'success': False,
                        'message': 'Введите имя пользвотеля при статусе выше register'
                    })
                user.username = request.data['username']
            else:
                user.username = None
            user.save()
            profile = FinanceProfile.objects.get_profile(user)
            profile.title = user.username
            profile.save()
        except IntegrityError:
            return Response({
            'success': False,
            'message': f'Данный ник уже занят'
        })
        return Response({
            'success': True,
            'message': f'Вы успешно поставили статус {user.verification} пользовотелю {user.email}'
        })