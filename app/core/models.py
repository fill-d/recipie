from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                       BaseUserManager, \
                                       PermissionsMixin


class UserMAnager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("user must have email adress")
        u = self.model(email=self.normalize_email(email), **extra_fields)
        u.set_password(password)
        u.save(using=self._db)
        return u

    def create_superuser(self, email, password):
        su = self.create_user(email, password)
        su.is_staff = True
        su.is_superuser = True
        su.save(using=self._db)
        return su


class User(AbstractBaseUser, PermissionsMixin):
    """ email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserMAnager()

    USERNAME_FIELD = 'email'
