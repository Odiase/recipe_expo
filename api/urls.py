from django.urls import path
from .views import get_routes, get_recipe, search_recipe

urlpatterns = [
    path("",get_routes, name = "api"),
    path("recipe/<str:id>/", get_recipe),
    path("recipe/search/<str:search_input>/", search_recipe)
]