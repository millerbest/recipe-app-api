"""
Tests for models.
"""

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model  # get default user model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creasting a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        # Create a new user using the UserModel's method
        user = get_user_model().objects.create_user(email=email, password=password)  # type: ignore

        # Check if the user's email is the same as the input
        self.assertEqual(user.email, email)

        # Check if the password is the same. Password is hashed, so we have to chck with
        # user.check_password method
        self.assertTrue(user.check_password(password))  # type: ignore

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")  # type: ignore
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")  # type: ignore

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser("teste@example.com", "test123")  # type: ignore

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user("test@example.com", "testpass123")
        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description.",
        )
        self.assertEqual(str(recipe), recipe.title)
