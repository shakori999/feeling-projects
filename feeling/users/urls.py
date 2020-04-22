from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [
    path("", include("django.contrib.auth.urls"), name="users"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logouts/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
]
