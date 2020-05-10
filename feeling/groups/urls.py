from django.urls import path, include
from . import views


app_name = "groups"
urlpatterns = [
    path("company/create/", views.CompanyCreate.as_view(), name="company-create"),
]
