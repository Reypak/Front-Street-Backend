from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from django.http import HttpResponse

from fs_utils.constants import APP_NAME, FROM_EMAIL


def send_templated_email(subject, template_name, context, recipient_list):
    message = render_to_string(template_name, context)

    email = EmailMessage(subject, message, FROM_EMAIL, recipient_list)
    email.content_subtype = "html"  # Indicate that the email content is HTML
    email.send()

    print("Sent email to:", recipient_list)


# def prepare_templated_email(subject, template_name, context, recipient_list):
#     message = render_to_string(template_name, context)
#     return (subject, message, FROM_EMAIL, recipient_list)


def send_test_email(request):
    if request.method == 'GET' and request.GET.get('email'):
        email = request.GET.get('email')
        subject = request.GET.get('subject')
        message = request.GET.get('message')

        subject = subject or APP_NAME
        message = message or "This is a test email."

        sender_name = "DevSystems"
        sender_email = settings.EMAIL_HOST_USER

        recipient_list = [email]

        send_mail(subject, message,
                  f"{sender_name} <{sender_email}>", recipient_list)

        # send_templated_email(
        #     subject, 'password_reset.html', {'name': 'Matt'}, recipient_list)

        return HttpResponse(f'Email sent successfully to: {email}')

    else:
        return HttpResponse("Invalid request.")
