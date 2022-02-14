from django.contrib import admin
from .models import CourseCoupon, Coupon, Order, OrderItem, Payment, CourseRecord, ContentRecord, QuizRecord

from ipm_learning.content.models import Course
from django.contrib.auth import get_user_model
from import_export.admin import ExportMixin, ImportExportModelAdmin 
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


User = get_user_model()


class CourseRecordResource(resources.ModelResource):
  email = fields.Field()
  course_name = fields.Field()

  class Meta:
    model = CourseRecord

  def dehydrate_email(self, cr):
    return cr.user.email

  def dehydrate_course_name(self, cr):
    return cr.course.name

@admin.register(CourseRecord)
class CourseRecordAdmin(ExportMixin, admin.ModelAdmin):
  fields = ('user','course')
  list_display = ('course', 'user', 'user_email', 'created_at')
  list_filter = ('course', 'user')
  resource_class = CourseRecordResource
  
  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ('reference_number', 'user', 'ordered_date', 'paid')
  list_filter = ('user', 'ordered_date', 'paid') 

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
  list_display = ('order', 'course')
  list_filter = ('order', 'course')

# @admin.register(Coupon)
# class CouponAdmin(admin.ModelAdmin):
#   list_display = ('code','amount')
  
@admin.register(CourseCoupon)
class CourseCouponAdmin(admin.ModelAdmin):
  list_display = ('code','course','amount','remaining_coupons')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  list_display = ('reference_number', 'order', 'amount', 'payment_method', 'payment_status', 'timestamp')
  list_filter = ('order', 'amount', 'payment_method', 'payment_status', 'timestamp') 

# @admin.register(CourseRecord)
# class CourseRecordAdmin(admin.ModelAdmin):
#   fields = ('user','course')
#   list_display = ('course', 'user', 'user_email', 'created_at')
#   list_filter = ('course', 'user')

@admin.register(ContentRecord)
class ContentRecordAdmin(admin.ModelAdmin):
  list_display = ('course_record','content', 'complete')
  list_filter = ('course_record','content', 'complete')

@admin.register(QuizRecord)
class QuizRecordAdmin(admin.ModelAdmin):
  list_display = ('course_record','content', 'complete')
  list_filter = ('course_record','content', 'complete')