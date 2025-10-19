from django.urls import path
from .views import intro_view, user_home_view

urlpatterns = [
    path("", intro_view, name="welcome"),
    path("home", user_home_view, name="home"),
]
