"""
Database models
"""

import uuid
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    # This function will be called when a new image is uploaded
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "recipe", filename)


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


class Recipe(models.Model):
    """Recipe object."""

    # ForeignKey allows to setup relationship between two models
    # settings.AUTH_USER_MODEL returns the user model defined in settings.py
    # models.CASCADE makes sure if a user is deleted, the related recipes are also deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")
    ingredients = models.ManyToManyField("Ingredient")
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
