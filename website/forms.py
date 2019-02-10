from django import forms
from .models import City


class AddPersonForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Your email', max_length=100)
    City.objects.all();
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
    )
