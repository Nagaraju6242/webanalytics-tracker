from .models import Track, TrackableEvent, TrackEvent
from django import forms
from django.contrib.auth.models import User


class TrackableEventForm(forms.ModelForm):
    class Meta:
        model = TrackableEvent
        fields = [
            "name",
            "type",
            "track_id",
            "html_id",
            "html_class",
            "html_tag",
            "html_selector",
        ]
        required = ["name", "type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "type": forms.Select(attrs={"class": "form-control mt-2"}),
            "track_id": forms.HiddenInput(),
            "html_id": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "html_class": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "html_tag": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "html_selector": forms.TextInput(attrs={"class": "form-control mt-2"}),
        }
