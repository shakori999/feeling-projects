from django import forms

from . import models


class ThoughtForm(forms.ModelForm):
    class Meta:
        fields = ["condition", "note"]
        model = models.Thought
