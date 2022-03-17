from allauth.account.views import PasswordResetView
from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.db.models.signals import post_save
from django.db import transaction

from ipm_learning.order.models import CourseRecord
from .models import CourseEmail, GroupEmail

# Helper func, ensures instance is committed before calling post_save
def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner


@receiver(post_save, sender=CourseEmail)
def send_course_email_now(sender, instance, created, **kwargs):
    
    email = instance
    if email.send_now:
        print(email.context)
        
        
@receiver(post_save, sender=GroupEmail)
def send_course_email_now(sender, instance, created, **kwargs):
    
    email = instance
    if email.send_now:
        print(email.context)


# Triggers Course Emails
@receiver(post_save,sender=CourseRecord)
def send_course_email(sender, instance, created, **kwargs):    
    
    if created:
        course_record = instance
        emails = course_record.course.emails.all()

        for email in emails:
            print(email.text_content)


# Triggers Group Emails
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@on_transaction_commit
def send_group_email(sender, instance, created, **kwargs):
    
    if created:
        user = instance
        groups = user.groups.all()
        
        for group in groups:
            emails = group.emails.all()
            for email in emails:
                print(email.text_content)


# Triggers password reset email
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@on_transaction_commit
def send_reset_password_email(sender, instance, created, **kwargs):
    
    def has_group(user, group):
        return user.groups.filter(name=group).exists()
      
    if created:
        u = instance
        group = "Upload-Users"
        if has_group(u, group): # Or has_groups(self.request.user, ["HelloDjango", "TEST"])
            
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