from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Token(models.Model):
    name = models.CharField(max_length=50)  # Имя криптовалюты, например, 'Solana'
    symbol = models.CharField(max_length=10)  # Символ криптовалюты, например, 'SOL'
    current_price_usd = models.DecimalField(max_digits=20, decimal_places=10)  # Текущая цена токена в долларах
    is_active = models.BooleanField(default=False)  # Флаг активности токена

    def __str__(self) -> models.CharField:
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),  # Пополнение баланса
        ('withdrawal', 'Withdrawal'),  # Вывод средств
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, совершающий транзакцию
    token = models.ForeignKey(Token, on_delete=models.CASCADE)  # Токен, используемый в транзакции
    amount_usd = models.DecimalField(max_digits=20, decimal_places=2)  # Сумма в долларах
    amount_token = models.DecimalField(max_digits=20, decimal_places=10)  # Сумма в токенах
    transaction_type = models.CharField(max_length=10,
                                        choices=TRANSACTION_TYPE_CHOICES)  # Тип транзакции: пополнение или вывод
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания транзакции
    status = models.CharField(max_length=20, default='pending')  # Статус транзакции: 'pending', 'completed' и т.д.

    def __str__(self) -> str:
        return f"{self.user.email} - {self.amount_usd} USD - {self.transaction_type}"


class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance_usd = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    balance_token = models.DecimalField(max_digits=20, decimal_places=10, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.user.email} - USD: {self.balance_usd}, Tokens: {self.balance_token}"

    def has_sufficient_balance(self, amount_usd: Decimal = None, amount_token: Decimal = None) -> bool:
        if amount_usd is not None and amount_usd > 0:
            if self.balance_usd < amount_usd:
                return False
        if amount_token is not None and amount_token > 0:
            if self.balance_token < amount_token:
                return False
        return True

    def deduct_balance(self, amount_usd: Decimal = None, amount_token: Decimal = None) -> bool:
        if not self.has_sufficient_balance(amount_usd, amount_token):
            return False
        if amount_usd is not None:
            self.balance_usd -= amount_usd
        if amount_token is not None:
            self.balance_token -= amount_token
        self.save()
        return True

    def add_balance(self, amount_usd=None, amount_token=None) -> None:
        if amount_usd is not None:
            self.balance_usd += amount_usd
        if amount_token is not None:
            self.balance_token += amount_token
        self.save()
