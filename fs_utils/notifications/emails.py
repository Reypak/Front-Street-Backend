from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings


def send_email(request):
    subject = 'Test Templated Email'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['reypak.sweg@gmail.com']

    context = {
        'user': 'Matthew',
        'message': 'This is a test email using an html templates.'
    }
    message = render_to_string('test.html', context)

    email = EmailMessage(subject, message, email_from, recipient_list)
    email.content_subtype = "html"
    email.send()

    return HttpResponse('Email sent successfully')
