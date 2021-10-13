from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.backends import JWTAuthenticationFinance

from .serializers import *

from accounts.models import User

from .models import FinanceProfile, Request, Transaction

from django.db.models import Q

class FinanceProfileView(APIView):

    authentication_classes = [JWTAuthenticationFinance]
    serializer = FinanceProfileSerializer

    def get(self, request, *args, **kwargs):
        profile = FinanceProfile.objects.get_profile(user=request.user)
        serializer = self.serializer(profile)
        return Response(serializer.data)
        
class TransactionsView(APIView):

    authentication_classes = [JWTAuthenticationFinance]
    serializer = TransactionDepthSerializer

    def get(self, request, *args, **kwargs):
        profile = FinanceProfile.objects.get_profile(user=request.user)
        transactions = Transaction.objects.filter(Q(from_profile=profile) | Q(to_profile=profile)).order_by('-id')
        serializer = self.serializer(transactions, many=True)
        return Response(serializer.data)
        

class TransactionView(APIView):

    authentication_classes = [JWTAuthenticationFinance]
    serializer = TransactionSerializer

    def post(self, request, *args, **kwargs):
        profile = FinanceProfile.objects.get_profile(user=request.user)
        data = request.data.copy()
        if not FinanceProfile.objects.filter(title=data['to_profile']).exists():
            return Response({
                'success': False,
                'message': 'Аккаунт не найден'
            }, status=400)
        if FinanceProfile.objects.get(title=data['to_profile']) == profile:
            return Response({
                'success': False,
                'message': 'Вы не можете отправить деньги самому себе'
            }, status=400)
        to_profile = FinanceProfile.objects.get(title=data['to_profile'])
        
        data['from_profile'] = f"{profile.id}"
        data['to_profile'] = f"{to_profile.id}"
        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['amount'] < 1:
            return Response({
                'success': False,
                'message': 'Нельзя отправить меньше 1 TLF'
            }, status=400)
        if serializer.validated_data['amount'] > profile.balance:
            return Response({
                'success': False,
                'message': 'У вас недостаточно средств'
            }, status=400)
        profile.balance -= serializer.validated_data['amount']
        to_profile.balance += serializer.validated_data['amount']
        to_profile.save()
        profile.save()
        serializer = TransactionDepthSerializer(serializer.save())
        return Response(serializer.data)
        
class GetTransactionView(APIView):

    authentication_classes = [JWTAuthenticationFinance]
    serializer = TransactionDepthSerializer

    def get(self, request, id):
        if not Transaction.objects.filter(id=id).exists():
            return Response({'success': False, 'message': 'Платеж не найден'})
        transaction = Transaction.objects.get(id=id)
        serializer = self.serializer(transaction)
        return Response(serializer.data)