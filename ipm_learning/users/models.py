from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from allauth.account.views import PasswordResetView
from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.db.models.signals import post_save
from django.db import transaction


class User(AbstractUser):
    """Default user for ipm_learning."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    phone_number = CharField(max_length=30)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@on_transaction_commit
def send_reset_password_email(sender, instance, created, **kwargs):
    
    def has_group(user, group):
        return user.groups.filter(name=group).exists()
    
    u = instance
    group = "Upload-Users"
    # group = 2
    
    print(u, u.groups.all())
        
    if created:
        if has_group(u, group): # Or has_groups(self.request.user, ["HelloDjango", "TEST"])
            print(u,group)
            # First create a post request to pass to the view
            request = HttpRequest()
            request.method = 'POST'

            # add the absolute url to be be included in email
            if settings.DEBUG:
                request.META['HTTP_HOST'] = '127.0.0.1:8000'
            else:
                request.META['HTTP_HOST'] = 'ibupunyamimpi.org'

            # pass the post form data
            request.POST = {
                'email': instance.email,
                'csrfmiddlewaretoken': get_token(HttpRequest())
            }
            PasswordResetView.as_view()(request)  # email will be sent!