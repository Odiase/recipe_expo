from django.db.models import Q
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe
from .serializers import RecipeSerializer

# Create your views here. 

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_routes(request): 
    context = {
        "GET":'/api/',
        "GET":'/api/recipe/:< recipe_id >/',
        "GET":"api/recipe/search/<search:word>/",
        "user":str(request.user),
        "auth":str(request.auth),
    }
    return Response(context)


@api_view(['GET'])
def get_recipe(request,id):
    recipe = Recipe.objects.get(id = id)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def search_recipe(request,search_input):
    if len(search_input) == 0 or search_input == "":
        return Response(status=500)
    search_results = Recipe.objects.filter(
        Q(recipe_name__icontains = search_input) |
        Q(category__icontains = search_input)
    )
    serializer = RecipeSerializer(search_results, many = True)
    return Response(serializer.data)