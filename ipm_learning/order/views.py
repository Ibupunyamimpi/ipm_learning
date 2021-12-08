from django.shortcuts import render
import datetime
import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views import generic
from .forms import CouponForm
from .models import OrderItem, Order, Payment, Coupon
from ipm_learning.content.models import Course
from .utils import get_or_set_order_session
from django.core.exceptions import ObjectDoesNotExist


class CartView(generic.TemplateView):
    template_name = "order/order_summary.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context

    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        if request.POST.get('promo-code'):
            promo_code = request.POST.get('promo-code')
            try:
                order.coupon = Coupon.objects.get(code=promo_code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("order:summary")
            except ObjectDoesNotExist:
                messages.info(request, "This coupon does not exist")
                return redirect("order:summary")
        else:
            messages.info(self.request, "Unknown Error")
            return redirect("order:summary")
    

class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("order:summary")

class PaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'order/payment.html'

    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        
        if request.POST.get('payment-code'):
            payment_method = 'Payment Code'
            payment_code = request.POST.get('payment-code')
            if payment_code == 'TESTCODE':
                payment_status = 'SUCCESS'
                # order.paid = True
                # order.ordered_date = datetime.date.today()
                # order.save()
            else:
                payment_status = 'FAILED'
        elif request.POST.get('bank-transfer'):
            payment_status = 'PENDING'
            payment_method = 'Bank Transfer'
        else:
            payment_status = 'FAILED'
            payment_method = 'Bank Transfer'
        
        payment = Payment.objects.create(
                order=order,
                payment_status=payment_status,
                amount=order.get_raw_order_total(),
                payment_method=payment_method
            )
    
        return redirect("order:success")

class ConfirmOrderView(generic.View):
    pass

    # def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#         course_id = request.POST.get('course_id')
#         course = Course.objects.get(pk=course_id)
#         course_record = CourseRecord(course=course, user=self.request.user)
#         course_record.save()
#         return redirect(course.contents.first())

class SuccessView(LoginRequiredMixin,generic.DetailView):
    template_name = 'order/success.html'
    context_object_name = 'payment'

    def get_object(self):
        user = self.request.user
        return Order.objects.filter(user=user).last().payments.last()

    def get_queryset(self):
        queryset = self.get_object()
        return queryset


class OrderListView(LoginRequiredMixin,generic.ListView):
    template_name = 'order/order_list.html'
    context_object_name = "orders"

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(
            user=user
        )
        return queryset





class AddCouponView(generic.View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, paid=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("order:order-summary")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("order:order-summary")