from django.urls import path
from .views import single_recipe, create_recipe, update_recipe, recipe_book, add_to_recipe_book, remove_recipe

urlpatterns = [
    path("create/", create_recipe, name = "create_recipe"),
    
    path("recipe_book/", recipe_book, name = "recipe_book"),
    path('add_to _recipe_book', add_to_recipe_book, name = "add_to_recipe_book"),
    path("remove_recipe/", remove_recipe, name = "remove_recipe"),

    path("update/<str:slug>/<str:id>/", update_recipe, name = "update_recipe"),
    path("<str:slug>/<str:id>/", single_recipe, name = "single_recipe"),
]