from django.contrib import admin
from .models import ComebackJourney
from ipm_learning.content.models import Course

class ComebackJourneyAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_count', 'signup_start_date', 'signup_end_date', 'course_start_date')

    def course_count(self, obj):
        """Return the count of related courses for the ComebackJourney."""
        return obj.courses.count()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'courses':
            kwargs['queryset'] = Course.objects.filter(is_comebackjourney=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(ComebackJourney, ComebackJourneyAdmin)
