from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import Model
from decimal import Decimal

from .manager import CustomUserManager


# class MainUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField('email address', unique=True)
#     username = None
#     code = models.IntegerField(default=0)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
#     winrate = models.IntegerField(default=0)
#     loserate = models.IntegerField(default=0)
#     tokenswin = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
#     tokenslose = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
#     deposits = models.IntegerField(default=0)
#
#     is_active = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_Seller = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return f'{self.email}'
#
#     def has_sufficient_balance(self, amount):
#         return self.balance >= amount
#
#     def deduct_balance(self, amount):
#         if self.has_sufficient_balance(amount):
#             self.balance -= Decimal(amount)
#             self.save()
#             return True
#         return False
#
#     def add_balance(self, amount):
#         self.balance += Decimal(amount)
#         self.save()


class MainUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = None
    code = models.IntegerField(default=0)
    winrate = models.IntegerField(default=0)
    loserate = models.IntegerField(default=0)
    tokenswin = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tokenslose = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    deposits = models.IntegerField(default=0)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_Seller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f'{self.email}'



# class Code(Model):
#     user_code = models.ForeignKey(MainUser, on_delete=models.CASCADE)
#     code = models.IntegerField()
