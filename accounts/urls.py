from django.urls import path
from .views import register, login, me,refresh_token

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("me/", me),
    path("token/refresh/", refresh_token)

]
