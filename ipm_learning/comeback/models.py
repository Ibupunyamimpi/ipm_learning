from django.db import models
from django.conf import settings
from django.contrib import admin

class ComebackJourney(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails/")
    weeks = models.PositiveIntegerField()
    cohort_size = models.PositiveIntegerField()
    remaining_spots = models.PositiveIntegerField()
    signup_start_date = models.DateField()
    signup_end_date = models.DateField()
    course_start_date = models.DateField()
    one_time_price = models.PositiveBigIntegerField()
    monthly_price = models.PositiveBigIntegerField()
    num_monthly_pmts = models.PositiveIntegerField()
    internal_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    courses = models.ManyToManyField('content.Course', related_name='comeback_journeys')
    
    def save(self, *args, **kwargs):
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
