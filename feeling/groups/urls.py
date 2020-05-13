from django.urls import path, include
from .views import company
from .views import family


company_patterns = [
    path("create/", company.Create.as_view(), name="create-com"),
    path("invite/", company.Invites.as_view(), name="invite-com"),
    path(
        "invite/<code>/<response>accept|reject/",
        company.InviteResponse.as_view(),
        name="invite-com-respone",
    ),
    path("edit/<slug:slug>", company.Update.as_view(), name="update-com"),
    path("detail/<slug:slug>", company.Detail.as_view(), name="detail-com"),
    path("leave/<slug:slug>", company.LeaveCompany.as_view(), name="leave-com"),
]

family_patterns = [
    path("create/", family.Create.as_view(), name="create-fam"),
    path("invite/", family.Invites.as_view(), name="invite-fam"),
    path(
        "invite/<code>/<response>accept|reject/",
        family.InviteResponse.as_view(),
        name="invite-fam-respone",
    ),
    path("edit/<slug:slug>", family.Update.as_view(), name="update-fam"),
    path("detail/<slug:slug>", family.Detail.as_view(), name="detail-fam"),
    path("leave/<slug:slug>", family.LeaveFamily.as_view(), name="leave-fam"),
]

app_name = "groups"

urlpatterns = [
    path("companies/", include(company_patterns), name="companies"),
    path("families/", include(family_patterns), name="families",),
]
