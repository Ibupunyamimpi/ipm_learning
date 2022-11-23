from django.contrib import admin
from .models import CourseCoupon, Coupon, Order, OrderItem, Payment, CourseRecord, ContentRecord, QuizRecord

from ipm_learning.content.models import Course
from django.contrib.auth import get_user_model
from import_export.admin import ExportMixin, ImportExportModelAdmin 
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


User = get_user_model()


class CourseRecordResource(resources.ModelResource):
  name = fields.Field()
  email = fields.Field()
  phone_number = fields.Field()
  course_name = fields.Field()
  

  class Meta:
    model = CourseRecord

  def dehydrate_name(self, cr):
    return cr.user.name
  
  def dehydrate_email(self, cr):
    return cr.user.email
  
  def dehydrate_phone_number(self, cr):
    return cr.user.phone_number
  
  def dehydrate_course_name(self, cr):
    return cr.course.name
  

@admin.register(CourseRecord)
class CourseRecordAdmin(ExportMixin, admin.ModelAdmin):
  def phone_number(self, obj):
        return obj.user.phone_number
      
  fields = ('user','course','tickets')
  list_display = ('course', 'user', 'user_email', 'phone_number', 'created_at', 'module_count', 'modules_complete', 'tickets')
  list_filter = ['course']
  search_fields = ('user__name','user__email','course__name')
  resource_class = CourseRecordResource

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ('reference_number', 'user', 'ordered_date', 'get_raw_order_total', 'paid')
  list_filter = ('ordered_date', 'paid')
  search_fields = ('id', 'user__name') 

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
  list_filter = ('payment_method', 'payment_status', 'timestamp') 
  search_fields = ('id','order__id')
  
  readonly_fields = ['courses','coupon']
  
  def courses(self, instance):
    return list(instance.order.order_items.all())
  
  def coupon(self, instance):
    return instance.order.course_coupon

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
  list_display = ('course_record','content', 'complete', 'quiz_questions', 'quiz_correct_ans', 'quiz_attempts')
  list_filter = ('course_record','content', 'complete')