from django.db import models
from django.conf import settings
from django.contrib import admin
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save



class ComebackJourney(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails/")
    weeks = models.PositiveIntegerField()
    cohort_size = models.PositiveIntegerField()
    remaining_spots = models.PositiveIntegerField(default=0)
    signup_start_date = models.DateField()
    signup_end_date = models.DateField()
    course_start_date = models.DateField()
    one_time_price = models.PositiveBigIntegerField()
    monthly_price = models.PositiveBigIntegerField()
    num_monthly_pmts = models.PositiveIntegerField()
    internal_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    courses = models.ManyToManyField('content.Course', related_name='comeback_journeys')
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)
    
   
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.is_active:
            # Set all other instances to inactive
            ComebackJourney.objects.filter(is_active=True).update(is_active=False)

        super(ComebackJourney, self).save(*args, **kwargs)
        
    def get_one_time_price(self):
        return "Rp {:,}".format(self.one_time_price).replace(',','.')
    
    def get_monthly_price(self):
        return "Rp {:,}".format(self.monthly_price).replace(',','.')
    
    def get_one_time_dsc(self):
        return (self.one_time_price / (self.monthly_price * self.num_monthly_pmts) - 1)
    
    def get_format_dsc(self):
        discount = self.get_one_time_dsc() * 100  # Convert ratio to percentage
        return "{:.0f}%".format(abs(discount))         # Format it as a rounded integer percentage

    def __str__(self):
        return self.title
    

    
class ComebackRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='comeback_records')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    comeback = models.ForeignKey('ComebackJourney', on_delete=models.CASCADE, related_name='comeback_records')
    is_monthly_pmt = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    one_time_price = models.PositiveBigIntegerField()
    monthly_price = models.PositiveBigIntegerField()
    num_monthly_pmts = models.PositiveIntegerField(default=0)
    pmts_completed = models.PositiveIntegerField(default=0)
    internal_notes = models.TextField(blank=True)
    
    
    def __str__(self):
        return f"COMEBACK-RECORD-{self.pk}-{self.comeback}-{self.user.email}"

    def reference_number(self):
        return f"COMEBACK-RECORD-{self.comeback}-{self.user}"


    @property
    @admin.display()
    def user_email(self):
        return self.user.email
    
    class Meta:
        unique_together = ('user', 'comeback',)


class ComebackWaitlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"COMEBACK-WAITLIST-{self.pk}-{self.user.email}"
    
@receiver(post_save, sender=ComebackRecord)
def update_waitlist(sender, instance, **kwargs):
    if instance.is_active:
        ComebackWaitlist.objects.filter(user=instance.user).delete()
        
        
@receiver(post_save, sender=ComebackJourney)
def create_course_records(sender, instance, **kwargs):
    from ipm_learning.order.models import CourseRecord
    # Get all courses associated with this comeback journey
    courses = instance.courses.all()  # Adjust to your field name holding the courses related to a ComebackJourney

    # Get all associated comeback_records
    comeback_records = ComebackRecord.objects.filter(comeback=instance)

    for comeback_record in comeback_records:
        for course in courses:
            # Check if a course record exists for the current comeback record and course
            course_record, created = CourseRecord.objects.get_or_create(
                course=course, 
                user=comeback_record.user,
                defaults={'comeback_record': comeback_record}
            )

            if not created and course_record.comeback_record != comeback_record:
                course_record.comeback_record = comeback_record
                course_record.save()

            # If a new course record was created, you might want to set additional attributes here before saving it
            if created:
                course_record.save()