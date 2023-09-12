from django.db import models
from ipm_learning.content.models import Course, Content, Event, Video, Text, Quiz, QuizQuestion
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime

from ipm_learning.comeback.models import ComebackRecord


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name='order_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)
    comeback_record = models.ForeignKey(ComebackRecord, on_delete=models.CASCADE, related_name='order_items_comeback', null=True, blank=True)
    tickets = models.IntegerField(default=1)
    
    def __str__(self):
        return self.reference_number
    
    def clean(self):
        if self.course and self.comeback_record:
            raise ValidationError("OrderItem cannot be linked to both a Course and a ComebackJourney.")
        if not self.course and not self.comeback_record:
            raise ValidationError("OrderItem must be linked to either a Course or a ComebackJourney.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def reference_number(self):
        associated_item = self.course or self.comeback_record
        return f"ORDER-ITEM-{self.pk}-{self.order}-{associated_item}-TICKETS:{self.tickets}"

    def get_item_price(self):
        if self.course:
            return self.course.price
        elif self.comeback_record:
            if self.comeback_record.is_monthly_pmt:
                return self.comeback_record.monthly_price
            else:
                return self.comeback_record.one_time_price
        else:
            return 0
    
    def get_discount_price(self):
        if self.course:
            return self.get_item_price() * (1 - (self.course.discount_pct)/100)
        elif self.comeback_record:
            return self.get_item_price()
        else:
            return 0
        
    # @property
    # def reference_number(self):
    #     return f"ORDER-ITEM-{self.pk}-{self.order}-{self.course}-TICKETS:{self.tickets}"

    # def get_item_price(self):
    #     return self.course.price

    # def get_discount_price(self):
    #     return self.get_item_price() * (1 - (self.course.discount_pct)/100)

    def get_amount_saved(self):
        return self.get_item_price() - self.get_discount_price()

    def get_raw_final_price(self):
        if self.course and self.course.discount_pct > 0:
            return self.tickets * self.get_discount_price()
        elif self.comeback_record:
            return self.tickets * self.get_item_price()
        else:
            return self.tickets * self.get_item_price()

    def get_order_item_total(self):
        total = self.get_raw_final_price()
        return "Rp {:,.0f}".format(total).replace(',','.')


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    course_coupon = models.ForeignKey(
        'CourseCoupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

    def get_order_item_count(self):
        return self.order_items.count()

    def get_raw_order_subtotal(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_raw_final_price()
        return total

    def get_raw_order_total(self):
        total = self.get_raw_order_subtotal()
        if self.course_coupon:
            total -= self.course_coupon.amount
        return total

    def get_order_subtotal(self):
        total = self.get_raw_order_subtotal()
        return "Rp {:,.0f}".format(total).replace(',','.')

    def get_order_total(self):
        total = self.get_raw_order_total()
        return "Rp {:,.0f}".format(total).replace(',','.')


class Payment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=(
        ('FlipID', 'FlipID'),
        ('Xendit', 'Xendit'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Payment Code', 'Payment Code'),
    ))
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=(
        ('SUCCESS', 'SUCCESS'),
        ('PENDING', 'PENDING'),
        ('FAILED', 'FAILED'),
    ))
    amount = models.PositiveIntegerField()
    raw_response = models.TextField(blank=True, null=True)
    invoice_url = models.URLField(blank=True, null=True)
    success_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"PAYMENT-{self.order}-{self.pk}"


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.code
    
    def get_amount(self):
        return "Rp {:,.0f}".format(self.amount).replace(',','.')
    
class CourseCoupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.PositiveIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_coupons')
    remaining_coupons = models.PositiveIntegerField()

    def __str__(self):
        return self.code

    @property
    def reference_number(self):
        return f"COURSE-COUPON-{self.course}-{self.code}"
    
    def get_amount(self):
        return "Rp {:,.0f}".format(self.amount).replace(',','.')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code'], name='unique_code')
        ]
    


class CourseRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='course_records')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_records')
    module_count = models.IntegerField(default=0)
    modules_complete = models.IntegerField(default=0)
    tickets = models.IntegerField(default=1)
    
    def __str__(self):
        return f"COURSE-RECORD-{self.pk}-{self.course.slug}-{self.user.email}"
        # return self.reference_number

    def reference_number(self):
        return f"COURSE-RECORD-{self.course}-{self.user}"
        # return f"COURSE-RECORD-{self.pk}-{self.course.slug}-{self.user.email}"

    @property
    @admin.display()
    def user_email(self):
        return self.user.email
    
    class Meta:
        unique_together = ('user', 'course',)


class ContentRecord(models.Model):
    course_record = models.ForeignKey(CourseRecord, on_delete=models.CASCADE, related_name='content_records')
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    quiz_questions = models.IntegerField(default=0)
    quiz_correct_ans = models.IntegerField(default=0)
    quiz_attempts = models.IntegerField(default=0)
    TYPE_CHOICES = [
    ('Generic-Content-Record', 'Generic-Content-Record'),
    ('Quiz-Record', 'Quiz-Record')
    ]
    content_type = models.CharField(max_length=25, choices=TYPE_CHOICES, default='Generic-Content-Record')

    def __str__(self):
        return f"ContentRecod-{self.pk}-{self.content.course.slug}-{self.content.slug}-{self.course_record.user.email}"

    class Meta:
        unique_together = ('course_record', 'content',)

class QuizRecordManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(content_type='QuizRecord')

class QuizRecord(ContentRecord):
    objects = QuizRecordManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        self.content_type = 'QuizRecord'
        return super(ContentRecord, self).save(*args, **kwargs)

    def __str__(self):
        return f"QuizRecord-{self.pk}-{self.content.course.slug}-{self.content.slug}-{self.course_record.user.email}"

@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, created, **kwargs):
    payment = instance
    order = payment.order
    if payment.payment_status == 'SUCCESS':
        order.paid = True
        order.ordered_date = datetime.datetime.now()
        order.save()
        
        if order.course_coupon:
            coupon = order.course_coupon
            coupon.remaining_coupons -= 1
            coupon.save()
        
        html_message = render_to_string('account/email/payment_success.html', {'context': 'order'})
        plain_message = strip_tags(html_message)
        subject="Payment Successful " + order.reference_number
        from_email=None
        to = order.user.email

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        

@receiver(post_save, sender=Order)
def create_course_record(sender, instance, created, **kwargs):
    order = instance
    if order.paid:
        for order_item in order.order_items.all():
            if order_item.course.multi_ticket and CourseRecord.objects.filter(course=order_item.course,user=order.user).exists():
                course_record = CourseRecord.objects.get(course=order_item.course,user=order.user)
                course_record.tickets += order_item.tickets
                course_record.save()
            else:
                course_record = CourseRecord(
                    course=order_item.course, 
                    user=order.user,
                    tickets=order_item.tickets)
                course_record.save()

@receiver(post_save, sender=CourseRecord)
def create_content_record(sender, instance, created, **kwargs):
    course_record = instance
    if created:
        for content in course_record.course.contents.all():
            if content.content_type == 'Quiz':
                content_complete = QuizRecord(course_record=course_record, content=content)
                content_complete.quiz_questions = content.quiz_questions.count()
                content_complete.content_type = 'Quiz-Record'
            else:
                content_complete = ContentRecord(course_record=course_record, content=content)
            content_complete.save()
        course_record.module_count = course_record.content_records.count()
        course_record.save()  

@receiver(post_save, sender=Content)
@receiver(post_save, sender=Video)
@receiver(post_save, sender=Event)
@receiver(post_save, sender=Text)
@receiver(post_save, sender=Quiz)
def add_content_record(sender, instance, created, **kwargs):
    new_content = instance
    
    for course_record in new_content.course.course_records.all():
        if not ContentRecord.objects.filter(course_record=course_record,content=new_content).exists():
            # print("New content created: ", new_content)
            # print("updating ", course_record)
            if new_content.content_type == 'Quiz':
                content_record = QuizRecord(course_record=course_record,content=new_content)
                content_record.quiz_questions = new_content.quiz_questions.count()
                content_record.content_type = 'Quiz-Record'
            else:
                content_record = ContentRecord(course_record=course_record,content=new_content)
            content_record.save()
            # print("Added content record: ", content_record)
            course_record.module_count = course_record.content_records.count()
            course_record.save()
            # print("Finished updating course record: ", course_record)

@receiver(post_delete, sender=Content)
@receiver(post_delete, sender=Video)
@receiver(post_delete, sender=Event)
@receiver(post_delete, sender=Text)
@receiver(post_delete, sender=Quiz)
def recount_course_record_modules(sender, instance, **kwargs):
    content = instance
    for course_record in content.course.course_records.all():
        course_record.module_count = course_record.content_records.count()
        course_record.modules_complete = course_record.content_records.filter(complete=True).count()
        course_record.save()
        
@receiver(post_save, sender=QuizQuestion)
def update_quiz_records(sender, instance, **kwargs):
    qq = instance
    quiz = qq.quiz
    quiz_records = QuizRecord.objects.filter(content=quiz)
    
    for qr in quiz_records:
        qr.quiz_questions = quiz.quiz_questions.count()
        qr.save()
        # print("Updated question count on ", qr)
    