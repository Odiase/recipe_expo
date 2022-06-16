from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from .models import Recipe, Comment, RecipeBook, Like
from .forms import RecipeForm

# Create your views here.

def search_recipe(request):
    if request.method == "POST":
        search_input = request.POST['search_input']
        if len(search_input) == 0:
            return redirect('search_recipe')
        recipes_results_by_name = Recipe.objects.filter(recipe_name__icontains = search_input)
        recipes_results_by_category = Recipe.objects.filter(category__icontains = search_input)
    else:
        recipes_results_by_name = ""
        recipes_results_by_category = ""

    context = {
        'search_result_by_name': recipes_results_by_name,
        'search_result_by_category':recipes_results_by_category,
        'search_input':search_input
    }
    return render(request,"recipes/search.html", context)


def single_recipe(request, slug, id):
    recipe = Recipe.objects.get(id = id)
    total_time = recipe.preparation_time + recipe.cooking_time
    recipe_comments = recipe.get_recent_comments()
    added_to_recipe_book = False
    liked_recipe = recipe.already_liked_recipe(request.user)

    # if the user is authentiucated, i check if the authenticated user has this recipe in his/her recipe book
    if request.user.is_authenticated:
        added_to_recipe_book = recipe.added_to_recipe_book(request.user)
        
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

    if recipe.user != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance = recipe)
        if form.is_valid():
            updated_recipe = form.save()
            return redirect('single_recipe',updated_recipe.slug, updated_recipe.id)
    context  = {
        'form':form
    }
    return render(request,"recipes/create_recipe.html", context)


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
            return HttpResponseNotFound()  
        recipe_book.recipes.add(recipe)
        return redirect('recipe_book')


def remove_recipe(request):
    if request.method == "POST":
        id = request.POST['recipe_id']
        try:
            recipe = Recipe.objects.get(id = id)
            recipe_book,created = RecipeBook.objects.get_or_create(user = request.user)
        except:
            return HttpResponseNotFound()  
        recipe_book.recipes.remove(recipe)
        return redirect('recipe_book')
    

def like_recipe(request,id):
    if request.method == "POST":
        recipe = Recipe.objects.get(id = id)
        if recipe.already_liked_recipe(request.user):
            return HttpResponseForbidden()
        new_like = Like.objects.create(user = request.user, recipe = recipe)
        return redirect('single_recipe', recipe.slug, id)