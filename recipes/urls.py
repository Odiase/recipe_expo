from django.urls import path
from .views import single_recipe, create_recipe, update_recipe, recipe_book, add_to_recipe_book, remove_recipe, like_recipe, search_recipe

urlpatterns = [
    path("write_a_recipe", create_recipe, name = "create_recipe"),
    path("search/", search_recipe, name = "search_recipe"),

    path("recipe_book/", recipe_book, name = "recipe_book"),
    path('add_to_recipe_book', add_to_recipe_book, name = "add_to_recipe_book"),
    path("remove_recipe/", remove_recipe, name = "remove_recipe"),

    path('like_recipe/<str:id>/',like_recipe, name = "like_recipe"),

    path("update/<str:slug>/<str:id>/", update_recipe, name = "update_recipe"),
    path("<str:slug>/<str:id>/", single_recipe, name = "single_recipe"),
]