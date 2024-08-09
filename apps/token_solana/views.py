from typing import Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Transaction, Token, UserBalance
from .serializers import TokenSerializer, TransactionSerializer, UserBalanceSerializer
from .utils import get_token_price

User = get_user_model()


class TokenViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Token] = Token.objects.all()
    serializer_class: TokenSerializer = TokenSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Transaction] = Transaction.objects.all()
    serializer_class: TransactionSerializer = TokenSerializer


class UserBalanceViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[UserBalance] = UserBalance.objects.all()
    serializer_class: UserBalanceSerializer = UserBalanceSerializer


@api_view(['POST'])
def add_balance(request: Request):
    user: User = request.user
    amount_usd: float = float(request.data.get('amount_usd'))

    try:
        token: Token = Token.objects.get(active=True)
    except Token.DoesNotExist:
        return Response({'error': 'Active token not fount'}, status=400)

    token_price: Union[float, None] = get_token_price(token.symbol)
    amount_token = amount_usd / token_price

    # Обновление или создание записи баланса пользователя
    user_balance, created = UserBalance.objects.get_or_create(user=user, token=token)
    user_balance.balance += amount_token
    user_balance.save()

    # Создание записи транзакции
    transaction = Transaction.objects.create(user=user, token=token, amount_usd=amount_usd, amount_token=amount_token)

    return Response({'amount_token': amount_token, 'new_balance': user_balance.balance}, status=200)