from django import forms
from .models import OrderItem
from ipm_learning.content.models import Course

class AddToCartForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        exclude = ['order','course']
        widgets = {'any_field': forms.HiddenInput(),}
        # fields = ['quantity', 'colour', 'size']

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your code',
    }))