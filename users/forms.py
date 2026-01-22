from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

COUNTRYCHOICES = [
    ("US", "United States"),
    ("RU", "Russia"),
]
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username")

class ProfileForm(forms.ModelForm):

    country = forms.ChoiceField(
        choices=[(name, name) for code, name in COUNTRYCHOICES],
        label="Country",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "username", "avatar", "country")
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.country:
            self.initial['country'] = self.instance.country