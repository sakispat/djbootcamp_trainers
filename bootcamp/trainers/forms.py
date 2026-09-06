"""Forms for creating and updating trainers."""

from django import forms
from .models import Trainer


class TrainerForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        strip=True,
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        strip=True,
        label="Last name",
    )

    subject = forms.CharField(
        max_length=50,
        strip=True,
        label="Subject",
    )

    class Meta:
        model = Trainer
        fields = (
            "first_name",
            "last_name",
            "subject",
        )