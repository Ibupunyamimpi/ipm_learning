from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from ipm_learning.users.forms import UserChangeForm, UserCreationForm

from django.http import HttpRequest
from allauth.account.views import PasswordResetView
from django.middleware.csrf import get_token
from django.conf import settings

User = get_user_model()

class UserUploadResource(resources.ModelResource):
    class Meta:
        model = User
        
    # def after_save_instance(self, instance, using_transactions, dry_run):
    #     print(self, instance)
        
    #     def send_reset_password_email(instance):
            
    #         def has_group(user, group):
    #             return user.groups.filter(id=group).exists()
        
    #         u = instance
    #         # group = "Upload-Users"
    #         group = 2
            
    #         print(u, u.groups.all())
                
    #         if has_group(u, group): # Or has_groups(self.request.user, ["HelloDjango", "TEST"])
    #             print(u,group)
    #             # First create a post request to pass to the view
    #             request = HttpRequest()
    #             request.method = 'POST'

    #             # add the absolute url to be be included in email
    #             if settings.DEBUG:
    #                 request.META['HTTP_HOST'] = '127.0.0.1:8000'
    #             else:
    #                 request.META['HTTP_HOST'] = 'ibupunyamimpi.org'

    #             # pass the post form data
    #             request.POST = {
    #                 'email': instance.email,
    #                 'csrfmiddlewaretoken': get_token(HttpRequest())
    #             }
    #             PasswordResetView.as_view()(request)  # email will be sent!
            
    #     if dry_run is False:
    #         send_reset_password_email(instance)
            
    
            
    
                
                
    # def after_save_instance(
    #     self, instance: User, using_transactions: bool, dry_run: bool,
    # ):
    #     super().after_save_instance(instance, using_transactions, dry_run)
    #     print('after_save')
    #     if dry_run is False:
    #         send_reset_password_email(instance)
                
                

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
        groups.short_description = 'Groups'
    
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('phone_number'),}),)
    
    list_display = ["username", "name", "email", "phone_number", "group", "is_superuser"]
    list_filter = ["groups"]
    search_fields = ["name", "email"]
    
    

# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):
#     pass