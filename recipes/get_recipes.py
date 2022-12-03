#stlib imports
import json
import requests

# third packages imports
from django.conf import settings


def api_recipe_search(search_input):
    """Searches and Returns Recipes From The Spoonacular Api"""

    api_key = settings.API_KEY
    api_recipe_data = ""
    base_uri = ""
    number_of_recipes_from_api = 0
    api_recipes = ""

    try:
        response = requests.get(f"https://api.spoonacular.com/recipes/search/?apiKey={api_key}&number=15&query={search_input}")
        api_recipe_data = json.loads(response.text) # getting the recipe_results from the response in python dictionary format
        api_recipes = api_recipe_data['results'] # recipes from api
        base_uri = api_recipe_data['baseUri'] # contains the url to the recipe images on spoonacular
        number_of_recipes_from_api = len(api_recipe_data['results'])
    except:
        pass
    
    context = {
        'num_of_recipes_from_api':number_of_recipes_from_api,
        "api_recipes": api_recipes,
        "base_uri":base_uri,
    }
    return context