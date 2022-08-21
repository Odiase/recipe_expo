import requests
import json

from django.shortcuts import render,redirect
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound

from .models import Recipe, Comment, RecipeBook, Like, ApiRecipe
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
            api_key = settings.API_KEY
            response = requests.get(f"https://api.spoonacular.com/recipes/search/?apiKey={api_key}&number=15&query={search_input}")
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

    # if the user is authenticated, i check if the authenticated user has this recipe in his/her recipe book
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
        return Http404()


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
    api_recipes = recipe_book.api_recipes.all()
    context = {
        'recipe_book': recipe_book,
        'book_recipes': book_recipes,
        'api_recipes':api_recipes
    }
    return render(request, "recipes/recipe-book.html", context)


@login_required(login_url="login")
def add_to_recipe_book(request):
    if request.method == "POST":
        id = request.POST['recipe_id']
        if request.POST['recipe_url']:
            url = request.POST['recipe_url']
            image = request.POST['recipe_image']
            name = request.POST['recipe_name']
            time = request.POST['recipe_time']
            link = request.POST['link']
        else:
            url = ""
            image = ""

        # try to get the recipe from the created Recipes in The Database
        # if it doesnt exist, try create an APiRecipe Object Instance with the submitted data and save.
        try:
            recipe = Recipe.objects.get(id = id)
            recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
            recipe_book.recipes.add(recipe)
        except:
            #create an api recipe instance
            api_recipe,created = ApiRecipe.objects.get_or_create(id = id, recipe_url = url, image_url = image, name = name, time_to_prepare = time, recipe_link = link)
            if RecipeBook.objects.filter(user = request.user, api_recipes = api_recipe).exists():
                return redirect('recipe_book')
            recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
            recipe_book.api_recipes.add(api_recipe)
        return redirect('recipe_book')
    else:
        return redirect("search_recipe")       

def remove_recipe(request):
    if request.method == "POST":
        id = request.POST['recipe_id']
        try:
            recipe = Recipe.objects.get(id = id)
            recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
            recipe_book.recipes.remove(recipe)
        except:
            api_recipe = ApiRecipe.objects.get(id = id)
            print(api_recipe)
            recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
            recipe_book.api_recipes.remove(api_recipe)
        return redirect('recipe_book')
    

@login_required(login_url="login")
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
    else:
        return redirect("home")