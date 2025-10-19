from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import logout_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomLoginForm

# Create your views here.


@never_cache
@logout_required(redirect_to="home")
def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = CustomLoginForm()
    return render(request, "users/user_login.html", {"form": form})


@never_cache
@login_required
def logout_view(request):
    logout(request)
    return redirect("welcome")


@never_cache
@logout_required(redirect_to="home")
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/user_signup.html", {"form": form})
