from django.core.management.base import BaseCommand
import requests
import WeatherEmail.passwords as passwords
import datetime
from website.models import Person
from django.template import loader
from django.core.mail import send_mail


# Command to send mail to everyone. Invoke with `python manage.py send_mail`
class Command(BaseCommand):
    help = 'Sends a weather update to everyone on our mailing list'
    # Store cities temperature as we go to save api calls.
    # Format: {<city name>: (<avg temp>, <current temp>, <precipitation rate (mm/hr)>)}
    # Example: {"Boston": (55, 50, 0)}
    cache = {}

    # Emails we will end up sending.
    # Format: {<email address>: {"subject": <subject>, "content": <content>}
    emails = {}

    template = loader.get_template("website/email_template.html")

    def handle(self, *args, **options):
        for person in Person.objects.all():
            email = person.email.replace("\'", "").replace(",", "").replace("(", "").replace(")", "")
            name = person.name.replace("\'", "").replace(",", "").replace("(", "").replace(")", "")
            city = person.city
            if name in self.cache:
                avg = self.cache[city][0]
                cur = self.cache[city][1]
                precip = self.cache[city][2]
            else:
                avg = avg_temp(city)
                cur = current(city)["temp"]
                precip = current(city)["precip"]
                self.cache[city] = [avg, cur, precip]

            context = {"name": name}
            if precip is (None or 0) or avg > cur + 5:
                context['subject'] = "It's nice out! Enjoy a discount on us."
            elif precip is not (None or 0) or avg < cur - 5:
                context['subject'] = "Not so nice out? That's okay, enjoy a discount on us."
            else:
                context['subject'] = "Enjoy a discount on us."

            self.emails[email] = {
                                     "subject": context['subject'],
                                     "content": self.template.render(context)
                                 }

        send_emails(self.emails)


# Send emails to the list. In the future if we have a lot of emails we
# could send a generic email and group it.
def send_emails(emails):
    for address in emails.keys():
        send_mail(
            subject=emails[address]['subject'],
            message="Message",
            html_message=emails[address]['content'],
            recipient_list=[address],
            from_email="kyleatyahoo@gmail.com",
        )


# Function to get current weather in a city. Not very scalable and should be turned into a
# bulk call if we have more than a few people on our mailing list.
# Returns {"temp": number, "precip": number}
# where first number is temperature (degrees f) and second number is mm/hr of precipitation
def current(city):
    api = f"http://api.weatherbit.io/v2.0/current?key={passwords.api_key()}&city={city}&country=US&units=I"
    r = requests.get(api)
    return {"temp": r.json()['data'][0]['temp'],
            "precip": r.json()['data'][0]['precip']}


# Function to get the average temp of a city.
def avg_temp(city):
    url = "http://api.weatherbit.io/v2.0/history/daily"
    now = datetime.datetime.now()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    start_date = f"{now.year}-{now.month}-{now.day}"
    end_date = f"{tomorrow.year}-{tomorrow.month}-{tomorrow.day}"

    api = f"{url}?key={passwords.api_key()}&start_date={start_date}&end_date={end_date}&city={city}&country=US&units=I"

    r = requests.get(api)
    return r.json()['data'][0]['temp']
