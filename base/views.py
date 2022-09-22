import random

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from recipes.models import Recipe,ApiRecipe
# from .forms import UserForm

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    popular_recipes = recipes[0:3]
    drinks = recipes.filter(category__icontains = "drinks")[0:3]
    pastries = recipes.filter(category__icontains = "pastries")[0:3]
    healthy_and_tasty = recipes.filter(category__icontains = "healthy")[0:3]

    # recipes to be displayed on home page
    featured_recipes = ApiRecipe.objects.all()[0:4]
    
    context = {
        "recipes":popular_recipes,
        "drinks":drinks,
        "pastries":pastries,
        "featured_recipes":featured_recipes,
        "healthy_and_tasty":healthy_and_tasty,
    }
    return render(request,'home.html', context)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if len(password1) <= 3 or len(password2) <=3:
                messages.error(request,"Password Is Too Short")
                return redirect("sign_up")
            if User.objects.filter(username = username).exists():
                messages.error(request,"This Username Is Taken")
                return redirect("sign_up")
            else:     
                user = User.objects.create_user(username = username, password = password1)
                messages.success(request,"Account Created Successfully!")
                login(request,user)
                return redirect('home')
        else:
            messages.error(request,"Passwords Don't Match")
            return redirect('sign_up')
    return render(request,'base/sign-up.html')


def Login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
             ###  CHECKING THE URL TO SEE IF THIS REDIRECTS THE USER TO ANOTHER PAGE
            if request.GET.get("next") != None:
                return redirect(request.GET.get("next"))
            else:
                messages.success(request,"Logged In Successfully")
                return redirect('home')
        else:
            messages.error(request,"Invalid Login Credentials")

    return render(request,'base/login.html')


def Logout(request):
    logout(request)
    
    return redirect('home')