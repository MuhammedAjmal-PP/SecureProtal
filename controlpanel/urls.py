from django.urls import path
from .views import (
    adminlogin_view,
    dashboard_view,
    adminlogout_view,
    usersmanagement_view,
    user_profile_view,
    admin_user_add,
    user_edit_view,
    user_delete_view,
)

urlpatterns = [
    path("login/", adminlogin_view, name="admin_login"),
    path("logout/", adminlogout_view, name="admin_logout"),
    path("", dashboard_view, name="admin_dashboard"),
    path("users", usersmanagement_view, name="users"),
    path("users/<int:pk>/", user_profile_view, name="profile"),
    path("user/add", admin_user_add, name="add_user"),
    path("users/edit/<int:pk>/", user_edit_view, name="user_edit"),
    path("users/<int:pk>/delete/", user_delete_view, name="user_delete"),
]
