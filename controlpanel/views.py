from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdminLoginForm, AdminUserCreationForm, AdminUserChangeForm
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse


# Create your views here.


# login View
@never_cache
def adminlogin_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admin_dashboard")

    if request.method == "POST":
        form = AdminLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect("admin_dashboard")
            else:
                messages.error(
                    request,
                    "You are not authorized to access the admin dashboard.",
                )
                return render(request, "admins/admin_login.html", {"form": form})
        else:
            messages.error(
                request,
                "Invalid username or password",
            )
            return render(request, "admins/admin_login.html", {"form": form})
    else:
        form = AdminLoginForm()
    return render(request, "admins/admin_login.html", {"form": form})


# Logout View
@never_cache
@login_required(login_url="admin_login")
def adminlogout_view(request):
    logout(request)
    return redirect("admin_login")


# Admin Home View
@never_cache
@login_required(login_url="admin_login")
def dashboard_view(request):

    if not request.user.is_superuser:
        return redirect("admin_login")

    thirty_days_ago = timezone.now() - timedelta(days=30)
    user_count = User.objects.count()
    new_signups_30d = User.objects.filter(date_joined__gte=thirty_days_ago).count()
    recent_users = User.objects.order_by("-date_joined")[:5]

    context = {
        "user_count": user_count,
        "new_signups_30d": new_signups_30d,
        "recent_users": recent_users,
        "page_title": "Dashboard Overview",
        "security_incidents": 5,
        "system_uptime": "99.9%",
    }
    return render(request, "admins/admin_dashboard.html", context)


# User Management View
@never_cache
@login_required(login_url="admin_login")
def usersmanagement_view(request):
    if not request.user.is_superuser:
        return redirect("admin_login")

    users = User.objects.all()
    query = request.GET.get("q")
    order_by = request.GET.get("order_by", "-date_joined")

    if query:
        users = users.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )

    orders = [
        "username",
        "-username",
        "date_joined",
        "-date_joined",
        "email",
        "-email",
        "last_login",
        "-last_login",
    ]

    if order_by in orders:
        users = users.order_by(order_by)
    else:
        users = users.order_by("-date_joined")

    # 30 items per page
    paginator = Paginator(users, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,  # Pass the Page object instead of the full QuerySet
        "users": page_obj.object_list,  # The list of users for the current page
        "page_title": "Manage Users",
        "total_users": users.count(),
        "current_order": order_by,
        "query": query,
    }
    return render(request, "admins/user_management.html", context)


# user profile view
@never_cache
@login_required(login_url="admin_login")
def user_profile_view(request, pk):
    if not request.user.is_superuser:
        return redirect("admin_login")

    user = get_object_or_404(User, pk=pk)

    context = {
        "user": user,
        "page_title": f"User Profile: {user.username}",
        "user_role": (
            "Superuser"
            if user.is_superuser
            else ("Staff" if user.is_staff else "Standard User")
        ),
    }

    return render(request, "admins/user_profile.html", context)


# admin user creation
@never_cache
@login_required(login_url="admin_login")
def admin_user_add(request):
    if not request.user.is_superuser:
        return redirect("admin_login")

    if request.method == "POST":
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'New user "{form.cleaned_data["username"]}" created successfully! 🎉',
            )
            return redirect(reverse("add_user"))
        else:
            messages.error(
                request,
                "There was an error creating the user. Please correct the fields below. ❌",
            )
    else:
        form = AdminUserCreationForm()

    context = {"form": form, "page_title": "Add New User"}

    return render(request, "admins/admin_userform.html", context)


# user edit view
@never_cache
@login_required(login_url="admin_login")
def user_edit_view(request, pk):
    if not request.user.is_superuser:
        return redirect("admin_login")

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = AdminUserChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'User "{user.username}" credentials updated successfully! Changes applied. 📝',
            )
            return redirect(reverse("profile", args=[pk]))
        else:
            messages.error(
                request,
                "There was an error updating the user. Please correct the fields below. ❌",
            )

    else:
        form = AdminUserChangeForm(instance=user)

    context = {"form": form, "user": user, "page_title": f"Edit User: {user.username}"}

    return render(request, "admins/admin_userform.html", context)


# USER DELETE VIEW
@never_cache
@login_required(login_url="admin_login")
def user_delete_view(request, pk):
    if not request.user.is_superuser:
        return redirect("admin_login")

    user_to_delete = get_object_or_404(User, pk=pk)

    # CRITICAL SECURITY CHECKS
    # 1. Prevent deleting self
    if user_to_delete == request.user:
        messages.error(request, "You cannot delete your own active admin account. 🛡️")
        return redirect(reverse("admin_users"))

    # 2. Prevent deleting superusers (unless you have a multi-superuser rule)
    if user_to_delete.is_superuser:
        messages.error(
            request, f"Cannot delete the primary Superuser: {user_to_delete.username}."
        )
        return redirect(reverse("admin_users"))

    if request.method == "POST":
        username = user_to_delete.username
        user_to_delete.delete()

        messages.success(request, f'User "{username}" was deleted successfully. 👋')
        return redirect(reverse("users"))

    # GET Request: Render Confirmation Page
    context = {
        "user": user_to_delete,
        "page_title": f"Confirm Delete: {user_to_delete.username}",
    }
    return render(request, "admins/user_delete_confirm.html", context)
