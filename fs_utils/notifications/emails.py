from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# from django.http import HttpResponse
# return HttpResponse('Email sent successfully')


def send_templated_email(subject, template_name, context, recipient_list, from_email=None):
    if from_email is None:
        from_email = settings.EMAIL_HOST_USER

    message = render_to_string(template_name, context)

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = "html"  # Indicate that the email content is HTML
    email.send()
