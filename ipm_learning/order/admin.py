from django.contrib import admin
from .models import Coupon, Order, OrderItem, Payment, CourseRecord, ContentRecord, QuizRecord

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ('reference_number', 'user', 'ordered_date', 'paid')
  list_filter = ('user', 'ordered_date', 'paid') 

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
  list_display = ('order', 'course')
  list_filter = ('order', 'course')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
  list_display = ('code','amount')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  list_display = ('reference_number', 'order', 'amount', 'payment_method', 'payment_status', 'timestamp')
  list_filter = ('order', 'amount', 'payment_method', 'payment_status', 'timestamp') 

@admin.register(CourseRecord)
class CourseRecordAdmin(admin.ModelAdmin):
  fields = ('user','course')
  list_display = ('course', 'user', 'created_at')
  list_filter = ('course', 'user')

@admin.register(ContentRecord)
class ContentRecordAdmin(admin.ModelAdmin):
  list_display = ('course_record','content', 'complete')
  list_filter = ('course_record','content', 'complete')

@admin.register(QuizRecord)
class QuizRecordAdmin(admin.ModelAdmin):
  list_display = ('course_record','content', 'complete')
  list_filter = ('course_record','content', 'complete')