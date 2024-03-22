"""
URL mappings for the redcipe app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)
router.register("tags", views.TagViewSet)
# enable auto-generated urls dependent on the ViewSet (for CRUD)

app_name = "recipe"  # used for reverse urls

# include(router.urls) automatcially generates urls from the router
urlpatterns = [path("", include(router.urls))]
