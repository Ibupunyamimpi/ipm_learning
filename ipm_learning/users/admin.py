from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from ipm_learning.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()

class UserUploadResource(resources.ModelResource):
    class Meta:
        model = User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):

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
    
    list_display = ["username", "name", "email", "is_superuser"]
    search_fields = ["name"]

# class UserAdmin(auth_admin.UserAdmin):