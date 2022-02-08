from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import SignupForm
from django import forms

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        # fields = admin_forms.UserCreationForm.Meta.fields + (
        #     'phone_number',
        # )
        
        fields = (
            "name",
            "email",
            "username",
            "phone_number",
        )
        
        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class SimpleSignupForm(SignupForm):
    name = forms.CharField(max_length=30)
    phone = forms.CharField(label="Phone Number", max_length=30)
    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.phone_number = self.cleaned_data['phone']
        user.save()
        return user