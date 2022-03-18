from django.db import models

#import for making Custom User Model
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):    #UserManager Class for Custom User

    #function for nomal user
    def create_user(self, username, email, password=None, **other_fields):

        if username is None:
            raise ValueError("You must provide an Username")

        if email is None:
            raise ValueError("You must provide an Email")

        user = self.model(username=username, email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save()
        return user

    #function for super user
    def create_superuser(self, username, email, password=None, **other_fields):

        if password is None:
            raise ValueError("Password should not be None")

        user = self.create_user(username, email, password)
        user.is_supersuer = True
        user.is_staff = True
        user.save()
        return user

#Custom Base User Model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index = True)   #'db_index'==True means it is indexable in db
    email = models.EmailField(max_length=255, unique=True,db_index = True)
    is_verified = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    #need a objects for Querying data and all.
    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self):
        return ' '