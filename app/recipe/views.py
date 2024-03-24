"""
Views for the recipe APIs
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    # ModelViewSet is specifically for Django models
    """View for manage recipe APIs (generates multiple endpoints)"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = (
        Recipe.objects.all()
    )  # The objects that are available for this viewset, here we get all recipes in the DB

    # Handling the authentication stuff
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):  # called when new recipe is created
        """Create a new recipe"""
        serializer.save(user=self.request.user)


class TagViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage tags in the database"""

    # Here we don't need ModelViewSet because it is not necessary. We only need the listing
    # functinality, using ModelViewSet is an overkill.

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # ListModelMixin provides the list method
    # GenericViewSet provides the basic viewset functionality
    # We can also use mixins.CreateModelMixin to provide the create method
    # We can also use mixins.RetrieveModelMixin to provide the retrieve method
    # We can also use mixins.UpdateModelMixin to provide the update method
    # We can also use mixins.DestroyModelMixin to provide the destroy method

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-name")


class IngredientViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage ingredients in the database"""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset by the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")
