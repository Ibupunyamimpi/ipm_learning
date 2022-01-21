from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('order-summary/', views.CartView.as_view(), name='summary'),
    path('order-list/', views.OrderListView.as_view(), name='order-list'),
    path('remove-from-cart/<pk>/',
         views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('confirm-order/', views.ConfirmOrderView.as_view(), name='confirm-order'),
    path('success/', views.SuccessView.as_view(), name='success'),
]