# from https://stackoverflow.com/questions/30068894/how-to-programmatically-trigger-password-reset-email-in-django-1-7-6
# myproject/myapp/management/commands/send_password_reset_emails.py
from django.core.management.base import BaseCommand, CommandError
# I use a custom user model, so importing that rather than the standard django.contrib.auth.models
# from users.models import User
from django.contrib.auth import get_user_model

from django.http import HttpRequest
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()


class Command(BaseCommand):
    help = 'Emails password reset instructions to all users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            try:
                if user.email:
                    print("Sending email for to this email:", user.email)
                    form = PasswordResetForm({'email': user.email})
                    assert form.is_valid()
                    request = HttpRequest()
                    request.META['SERVER_NAME'] = 'www.example.com'
                    request.META['SERVER_PORT'] = 443
                    form.save(
                        request= request,
                        use_https=True,
                        from_email="admin@mysite.com", 
                        email_template_name='account/email/password_reset_key_message.html',
                        # email_template_name='account/email/bulk_password_reset.html',
                        extra_email_context = {"username": user.username}
                        )
                    
            except Exception as e:
                print(e)
                continue

        return 'done'