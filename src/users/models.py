__author__ = 'dmalik'

from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass

class User(AbstractUser):
    pass
