from django.urls import path
from .views import home, sign_up, Logout, Login

urlpatterns = [
    path('', home, name = "home"),
    path('sign-up/', sign_up, name = "sign_up"),
    path('login/', Login, name ="login"),
    path('logout/',Logout, name = "logout"),
]