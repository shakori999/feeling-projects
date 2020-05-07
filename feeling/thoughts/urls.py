from django.urls import path

from . import views

app_name = "thoughts"
urlpatterns = [
    path("create/", views.CreateThought.as_view(), name="create"),
]
