from django.contrib import admin
from .models import ComebackJourney, ComebackRecord, ComebackWaitlist
from ipm_learning.content.models import Course
from import_export.admin import ExportMixin
from import_export import resources

class ComebackJourneyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'course_count', 'signup_start_date', 'signup_end_date', 'course_start_date')

    def course_count(self, obj):
        """Return the count of related courses for the ComebackJourney."""
        return obj.courses.count()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'courses':
            kwargs['queryset'] = Course.objects.filter(is_comebackjourney=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# class ComebackRecordAdmin(admin.ModelAdmin):
    # list_display = ('user', 'comeback', 'is_active', 'is_monthly_pmt', 'pmts_completed', 'created_at')
    # fieldsets = (
    #     (None, {'fields': ('user', 'comeback', 'is_active')}),
    #     ('Payment Info', {'fields': ('one_time_price', 'monthly_price', 'is_monthly_pmt', 'pmts_completed', 'created_at')}),
    #     ('Internal Notes', {'fields': ('internal_notes',)}),
    # )
    # readonly_fields = ('created_at',)



class ComebackWaitlistResource(resources.ModelResource):
    class Meta:
        model = ComebackWaitlist
        fields = ('user__username', 'user__email', 'user__phone_number', 'created_at')

class ComebackWaitlistAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'user_email', 'user_phone_number', 'created_at')
    resource_class = ComebackWaitlistResource

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def user_phone_number(self, obj):
        # Assuming phone_number is a field on your user model
        return obj.user.phone_number  
    user_phone_number.short_description = 'User Phone Number'



admin.site.register(ComebackJourney, ComebackJourneyAdmin)
# admin.site.register(ComebackRecord, ComebackRecordAdmin)
admin.site.register(ComebackWaitlist, ComebackWaitlistAdmin)