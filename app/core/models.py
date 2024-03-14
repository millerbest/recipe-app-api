"""
Database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""

        # user cannot have empty email address
        if not email:
            raise ValueError("User must have an email address.")

        # self.model is the UserModel
        # normalize email before the email is stored (build-in function from BaseUserManager)
        user = self.model(email=self.normalize_email(email), **extra_fields)

        # It will encrypted the password and save to the user
        user.set_password(password)

        # self._db refers to the DB to save the new user, if we want to implement
        # multiple dbs, here should be changed
        user.save(using=self._db)
        return user

    # Support creating superuser, superuser should be is_staff == True and is_superuser == True
    def create_superuser(self, email, password=None, **extra_fields):
        """Create, save and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# AbstractBaseUser for the auth system and PermissionsMixin for the permission features of Django
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False
    )  # if the user can login to Django Admin

    # Assign the user manager
    objects = UserManager()

    USERNAME_FIELD = "email"  # replace the default field, which is username
