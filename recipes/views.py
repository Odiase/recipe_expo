from ast import If
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotFound

from .models import Recipe, Comment, RecipeBook
from .forms import RecipeForm

# Create your views here.

def single_recipe(request, slug, id):
    recipe = Recipe.objects.get(id = id)
    total_time = recipe.preparation_time + recipe.cooking_time
    recipe_comments = recipe.get_recent_comments()

    if request.method == "POST":
        message = request.POST['comment_message']
        new_comment = Comment.objects.create(user = request.user,recipe = recipe, message = message)
        new_comment.save()
        return redirect("single_recipe",slug, id)
    
    context = {
        'recipe':recipe,
        'total_time':total_time,
        'recipe_comments':recipe_comments,
        'num_of_comments':recipe_comments.count()
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


######## recipe book functionality
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
