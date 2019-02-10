from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Person, City
from .emailing import email_everyone
from .forms import AddPersonForm


def index(request):
    if request.method == 'POST':
        form = AddPersonForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            name = form.cleaned_data['name'],
            email = form.cleaned_data['email'],

            if Person.objects.filter(email=email).exists():
                return HttpResponseRedirect("bad-email/")
            if not City.objects.filter(name=city).exists():
                return HttpResponseRedirect("bad-city/")
            city = City.objects.get(name=city)
            city.person_set.create(name=name, email=email)
            return HttpResponseRedirect("success/")
    else:
        form = AddPersonForm()
        return render(request, 'website/index.html', {'form': form})
    return HttpResponseRedirect('error/')


def error(request):
    return HttpResponse("There was an issue with your form. Please try again.")


def repeat_email(request):
    return HttpResponse("You have already signed up.")


def invalid_city(request):
    return HttpResponse("City not supported.")


def success(request):
    return HttpResponse("Thanks for signing up!")


def send(request):
    email_everyone()
    return HttpResponse("Nice! You sent everyone an email!");
