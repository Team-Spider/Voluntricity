from dotenv import load_dotenv
import os
from django.core.mail import EmailMessage

load_dotenv()

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject = data['email_subject'],
            body = data['email_body'],
            from_email = os.environ.get('EMAIL_HOST_USER'),
            to = [data['to_email']]
        )
        email.send()