from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.decorators import logout_required

# Create your views here.

@never_cache
@logout_required(redirect_to="home")
def intro_view(request):
    return render(request, "users/welcome.html")


@never_cache
@login_required(login_url="login")
def user_home_view(request):
    return render(request, "users/user_home.html")

