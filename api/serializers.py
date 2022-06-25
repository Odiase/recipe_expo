from rest_framework.serializers import ModelSerializer
from recipes.models import Recipe

class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'recipe_name','recipe_info', 'recipe_image', 'recipe_preparation', 'preparation_time', 'cooking_time', 'category', 'serving']