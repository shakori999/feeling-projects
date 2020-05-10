from django.urls import path, include
from .views import company
from .views import family

company_patterns = [
    path("create/", company.Create.as_view(), name="create"),
    path("edit/<slug:slug>", company.Update.as_view(), name="update"),
    path("detail/<slug:slug>", company.Detail.as_view(), name="detail"),
]

app_name = "groups"

urlpatterns = [
    path("companies/", include(company_patterns), name="companies",),
]
