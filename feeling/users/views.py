from django.shortcuts import render, reverse
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.urls import reverse_lazy
from braces.views import SelectRelatedMixin
from django.contrib.auth.models import User

# Create your views here.
class Dashboard(LoginRequiredMixin, SelectRelatedMixin, generic.TemplateView):
    model = User
    select_related = "thoughts"
    template_name = "users/dashboard.html"

    def get_objects(self, query=None):
        return self.request.user


class LogoutView(LoginRequiredMixin, generic.FormView):
    form_class = forms.LogoutForm
    template_name = "users/logout.html"

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse("home"))


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:dashboard")
