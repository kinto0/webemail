from django.core.mail import EmailMessage


def email_everyone():
    email = EmailMessage('title', 'body', to=['kyleatyahoo@gmail.com'])
    email.send()