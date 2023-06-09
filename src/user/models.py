from typing import Any, Optional
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models


class CustomerUserManager(UserManager):
    def create_user(self, username: str, password: str, email: str | None = None, **kwargs) -> Any:
        return self._create_user(username, email, password, **kwargs)



class User(AbstractBaseUser):
    friends = models.ManyToManyField(to='user.User', related_name='+')
    username = models.CharField(max_length=512, db_index=True, unique=True)
    email = models.CharField(max_length=255, null=True)

    objects =  CustomerUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
