from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from .. import forms

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
