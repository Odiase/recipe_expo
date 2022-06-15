from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from recipes.models import Recipe
# from .forms import UserForm

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()

    context = {
        "recipes":recipes,
    }
    return render(request,'home.html', context)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    # form = UserForm()
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
                user.save()
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
            return redirect('home')
        else:
            messages.error(request,"Invalid Login Credentials")

    return render(request,'base/login.html')


def Logout(request):
    logout(request)
    return redirect('home')