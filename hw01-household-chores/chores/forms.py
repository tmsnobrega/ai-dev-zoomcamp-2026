"""Validate the two small forms used by the application."""

from django import forms

from .models import Chore, Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name"]


class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ["title", "description", "assignee", "due_date"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}
