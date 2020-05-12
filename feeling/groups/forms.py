from django import forms
from .models import *

# from django.contrib.auth.models import User
from django.db.models import Q
from . import models


class FamilyForm(forms.ModelForm):
    class Meta:
        fields = ("name", "description")
        model = Family


class CompanyForm(forms.ModelForm):
    class Meta:
        fields = ("name", "description")
        model = Company


class CompanyInviteForm(forms.Form):
    email_or_username = forms.CharField(label="Email or username")

    def clean_email_or_username(self):
        data = self.cleaned_data["email_or_username"]
        try:
            self.invite = models.User.objects.get(Q(email=data) | Q(username=data))
        except models.User.DoesNotExist:
            raise ValueError("No such user")
        return data
