"""
Views for the recipe APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    # ModelViewSet is specifically for Django models
    """View for manage recipe APIs (generates multiple endpoints)"""
    serializer_class = serializers.RecipeSerializer
    queryset = (
        Recipe.objects.all()
    )  # The objects that are available for this viewset, here we get all recipes in the DB

    # Handling the authentication stuff
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-id")
