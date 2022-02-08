from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ipm_learning.order.models import Order
import io, csv

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        queryset = Order.objects.filter(
            user=user
        )
        context["orders"] = queryset
        return context
  


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name", "phone_number"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class BulkUploadView(TemplateView):
    def get(self, request):
        template_name = 'users/bulk_import.html'
        return render(request, template_name)

    def post(self, request):
        paramFile = io.TextIOWrapper(request.FILES['userfile'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            User(
                name=row['name'],
                username=row['email'],
                email=row['email'],
            )
            for row in list_of_dict
        ]
        try:
            msg = User.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ', e)
            returnmsg = {"status_code": 500}
            
        # html_message = render_to_string('account/email/payment_success.html', {'context': 'user'})
        # plain_message = strip_tags(html_message)
        # subject="Welcome to the new Ibu Punya Mimpi"
        # from_email=None
        # to = user.email

        # send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return JsonResponse(returnmsg)