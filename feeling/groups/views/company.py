from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from .. import forms
from ..models import Family
from .. import models

# from ..models import Company
from braces.views import SetHeadlineMixin

# Create your views here.
class Create(LoginRequiredMixin, SetHeadlineMixin, generic.CreateView):
    form_class = forms.CompanyForm
    headline = "create company"
    # success_url = reverse_lazy("users:dashboard")
    template_name = "companies/Company_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response


class Update(LoginRequiredMixin, SetHeadlineMixin, generic.UpdateView):
    form_class = forms.CompanyForm
    success_url = reverse_lazy("users:dashboard")
    template_name = "companies/Company_form.html"

    def get_queryset(self):
        return self.request.user.companies.all()

    def get_headline(self):
        return f"edit {self.object.name}"

    def get_success_url(self):
        return reverse("groups:detail-com", kwargs={"slug": self.object.slug})


class Detail(LoginRequiredMixin, generic.FormView):
    form_class = forms.CompanyInviteForm
    headline = "Detail"
    template_name = "companies/detail.html"

    def get_queryset(self):
        return self.request.user.companies.all()

    def get_object(self):
        self.object = self.request.user.companies.get(slug=self.kwargs.get("slug"))
        return self.object

    def get_success_url(self):
        self.get_object()
        return reverse("groups:detail-com", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        models.CompanyInvite.objects.create(
            from_user=self.request.user, to_user=form.invite, company=self.get_object(),
        )
        return response


class Invites(LoginRequiredMixin, generic.ListView):
    template_name = "companies/invite.html"

    def get_queryset(self):
        return self.request.user.companyinvite_receved.filter(accepted=0)


class InviteResponse(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy("groups:invite-com")

    def get(self, request, *args, **kwargs):
        invite = get_object_or_404(
            models.CompanyInvite,
            to_user=request.user,
            uuid=kwargs.get("code"),
            accepted=0,
        )
        if kwargs.get("response") == "accept":
            invite.accepted = 1
        else:
            invite.accepted = 2

        invite.save()
        return super().get(request, *args, **kwargs)
