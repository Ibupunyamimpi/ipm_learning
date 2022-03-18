from allauth.account.views import PasswordResetView
from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.db.models.signals import post_save
from django.db import transaction

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from ipm_learning.order.models import CourseRecord
from .models import CourseEmail, GroupEmail
from django.contrib.auth import get_user_model

User = get_user_model()


"""

Helper Methods

"""

# Ensures instance is committed before calling post_save
def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner

def email_sender(email, user):
    html_message = render_to_string('emails/email_template.html', {'context': email.text_content})
    plain_message = strip_tags(html_message)
    subject= "[Ibu Punya Mimpi] " + email.subject
    from_email= None
    to = user.email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


"""

CourseEmail

"""

# Send CourseEmail immediately
@receiver(post_save, sender=CourseEmail)
def send_course_email_now(sender, instance, created, **kwargs):
    email = instance
    if email.send_now:
        course = email.course
        course_records = course.course_records.all()
        for cr in course_records:
            email_sender(email, cr.user)
        email.send_now = False
        email.save()
 
 
 # Triggers Course Emails on CourseRecord create
@receiver(post_save,sender=CourseRecord)
def send_course_email(sender, instance, created, **kwargs):    
    
    if created:
        course_record = instance
        user = course_record.user
        emails = course_record.course.emails.all()
        for email in emails:
            email_sender(email, user)



"""

GroupEmail

"""

# Send GroupEmail immediately
@receiver(post_save, sender=GroupEmail)
def send_group_email_now(sender, instance, created, **kwargs):
    email = instance
    if email.send_now:
        group = email.group
        print(group)
        users = User.objects.filter(groups__name=group)
        for user in users:
            email_sender(email, user)
        email.send_now = False
        email.save()

# Triggers Group Emails on User create
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@on_transaction_commit
def send_group_email(sender, instance, created, **kwargs):
    
    if created:
        user = instance
        groups = user.groups.all()
        
        for group in groups:
            emails = group.emails.all()
            for email in emails:
                email_sender(email, user)


# Triggers password reset email for Users created in the "Upload-Users" Group
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