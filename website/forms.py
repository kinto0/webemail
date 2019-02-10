from django import forms


class AddPersonForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Your email', max_length=100)
    city = forms.CharField(label='Your city', max_length=100)
