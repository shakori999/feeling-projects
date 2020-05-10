from django import forms
from .models import *


class FamilyForm(forms.ModelForm):
    class Meta:
        fields = ("name", "description")
        model = Family


class CompanyForm(forms.ModelForm):
    class Meta:
        fields = ("name", "description")
        model = Company
