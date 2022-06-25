import requests
import json

from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden, HttpResponseNotFound

from .models import Recipe, Comment, RecipeBook, Like
from .forms import RecipeForm

# Create your views here.

def search_recipe(request):

    if request.method == "POST":
        search_input = request.POST['search_input']

        if len(search_input) == 0:
            return redirect('search_recipe')       
        elif len(search_input) == 1:
            search_results = Recipe.objects.filter(
            Q(recipe_name__startswith = search_input) |
            Q(category__startswith = search_input)
        )
        else:
            search_results = Recipe.objects.filter(
            Q(recipe_name__icontains = search_input) |
            Q(category__icontains = search_input)
        )

        # api recipes search
        try:
            response = requests.get(f"https://api.spoonacular.com/recipes/search/?apiKey=e2f87062025142ed9320f04299f79ed4&number=15&query={search_input}")

            api_recipe_data = json.loads(response.text) # getting the recipe_results from the response in python dictionary format

            api_recipes = api_recipe_data['results']

            base_uri = api_recipe_data['baseUri'] # needed to get the recipe images in the image src attribute on the frontend

            number_of_recipes_from_api = len(api_recipe_data['results'])
        except:
            api_recipe_data = ""
            base_uri = ""
            number_of_recipes_from_api = 0
            api_recipes = ""
    else:
        search_results = ""
        search_input = ""
        empty_search = False

        #api variables
        api_recipe_data = ""
        base_uri = ""
        number_of_recipes_from_api = 0
        api_recipes = ""

    context = {
        'search_results':search_results,
        'search_input':search_input,
        'number_of_results':len(search_results) + number_of_recipes_from_api,
        "api_recipes": api_recipes,
        "base_uri":base_uri,
    }
    return render(request,"recipes/search.html", context)


def single_recipe(request, slug, id):
    try:
        recipe = Recipe.objects.get(id = id)
    except:
        return HttpResponseNotFound()
    total_time = recipe.preparation_time + recipe.cooking_time
    recipe_comments = recipe.get_recent_comments()[0:5]
    added_to_recipe_book = False
    liked_recipe = False

    # if the user is authentiucated, i check if the authenticated user has this recipe in his/her recipe book
    if request.user.is_authenticated:
        added_to_recipe_book = recipe.added_to_recipe_book(request.user)
        liked_recipe = recipe.already_liked_recipe(request.user)
        
    # comment functionality
    if request.method == "POST":
        message = request.POST['comment_message']
        new_comment = Comment.objects.create(user = request.user,recipe = recipe, message = message)
        new_comment.save()
        return redirect("single_recipe",slug, id)
    
    context = {
        'recipe':recipe,
        'total_time':total_time,
        'recipe_comments':recipe_comments,
        'num_of_comments':recipe_comments.count(),
        'in_recipe_book': added_to_recipe_book,
        'liked_recipe':liked_recipe,
    }
    return render(request,"recipes/single-recipe.html", context)


@login_required(login_url="login")
def create_recipe(request):
    form = RecipeForm()

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit = False)
            new_recipe.user = request.user
            new_recipe.save()

            recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
            recipe_book.recipes.add(new_recipe)
            return redirect('single_recipe',new_recipe.slug, new_recipe.id)
    context  = {
        'form':form
    }
    return render(request,"recipes/create_recipe.html", context)


@login_required(login_url="login")
def update_recipe(request,slug,id):
    try:
        recipe = Recipe.objects.get(id = id)
        form = RecipeForm(instance=recipe)
    except:
        return HttpResponseNotFound()

    # verifying that the request user is the writer of this recipe
    if recipe.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance = recipe)
        if form.is_valid():
            updated_recipe = form.save()
            return redirect('single_recipe',updated_recipe.slug, id)
    context  = {
        'form':form,
        'recipe_name':recipe.recipe_name
    }
    return render(request,"recipes/update_recipe.html", context)


######## recipe book functionalities

@login_required(login_url="login")
def recipe_book(request):
    recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
    book_recipes = recipe_book.recipes.all()
    context = {
        'recipe_book': recipe_book,
        'book_recipes': book_recipes,
    }
    return render(request, "recipes/recipe-book.html", context)


@login_required(login_url="login")
def add_to_recipe_book(request):
    if request.method == "POST":
        id = request.POST['recipe_id']
        try:
            recipe = Recipe.objects.get(id = id)
            recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
        except:
            return Http404()  
        recipe_book.recipes.add(recipe)
        return redirect('recipe_book')
        

def remove_recipe(request):
    if request.method == "POST":
        id = request.POST['recipe_id']
        try:
            recipe = Recipe.objects.get(id = id)
            recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
        except:
            return Http404()  
        recipe_book.recipes.remove(recipe)
        return redirect('recipe_book')
    

def like_recipe(request,id):
    if request.method == "POST":
        try:
            recipe = Recipe.objects.get(id = id)
        except:
            return Http404()
        if recipe.already_liked_recipe(request.user): # checking if the recipe is already liked by the request user
            return HttpResponseForbidden()
        new_like = Like.objects.create(user = request.user, recipe = recipe)
        return redirect('single_recipe', recipe.slug, id)