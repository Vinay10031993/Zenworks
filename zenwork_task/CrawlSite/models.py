from django.db import models

# Create your models here.
from django.utils.translation import pgettext_lazy
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)

import datetime
class User(AbstractBaseUser):
    email = models.CharField(pgettext_lazy('User field', 'email'), max_length=50, unique=True)
    addresses = models.CharField(pgettext_lazy('User field', 'address'), null=True, max_length=50)
    phone = models.CharField(pgettext_lazy('Phone Field', 'Phone Number'),max_length=15, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)
    username = models.CharField(pgettext_lazy('User field', 'username'), max_length=50, unique=True)
    password = models.CharField(pgettext_lazy('User field', 'password'), max_length=50)
    USERNAME_FIELD = 'username'

    # class Meta:
    #     verbose_name = pgettext_lazy('User model', 'user')

class UserToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="related to unique user",
        )
    access_token = models.CharField("user's login unique access token", max_length=255, unique=True)
    last_queried_on = models.DateTimeField(null=True)
    expires_at = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=5))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
