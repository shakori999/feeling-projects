from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from .. import forms
from .. import models

# from ..models import Family
from braces.views import SetHeadlineMixin

# Create your views here.
class Create(LoginRequiredMixin, SetHeadlineMixin, generic.CreateView):
    form_class = forms.FamilyForm
    headline = "create Family"
    success_url = reverse_lazy("users:dashboard")
    template_name = "families/families_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response


class Update(LoginRequiredMixin, SetHeadlineMixin, generic.UpdateView):
    form_class = forms.FamilyForm
    # success_url = reverse_lazy("users:dashboard")
    template_name = "families/families_form.html"

    def get_queryset(self):
        return self.request.user.families.all()

    def get_headline(self):
        return f"edit {self.object.name}"

    def get_success_url(self):
        return reverse("groups:detail-fam", kwargs={"slug": self.object.slug})


class Detail(LoginRequiredMixin, generic.DetailView):
    headline = "Detail"
    template_name = "families/detail.html"

    def get_queryset(self):
        return self.request.user.families.all()


class LeaveFamily(LoginRequiredMixin, SetHeadlineMixin, generic.FormView):
    form_class = forms.LeaveForm
    template_name = "families/leave.html"
    success_url = reverse_lazy("users:dashboard")

    def get_object(self):
        try:
            self.object = (
                self.request.user.families.filter(slug=self.kwargs.get("slug"),)
                .exclude(created_by=self.request.user)
                .get()
            )
        except models.Family.DoesNotExist:
            raise Http404

    def get_headline(self):
        self.get_object()
        return f"Leave {self.object} ?"

    def form_valid(self, form):
        self.get_object()
        self.object.members.remove(self.request.user)
        return super().form_valid(form)


class Invites(LoginRequiredMixin, generic.ListView):
    model = models.FamilyInvite
    template_name = "families/invite.html"

    def get_queryset(self):
        return self.request.user.familyinvite_receved.filter(accepted=0)


class InviteResponse(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy("groups:invite-fam")

    def get(self, request, *args, **kwargs):
        invite = get_object_or_404(
            models.FamilyInvite,
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
