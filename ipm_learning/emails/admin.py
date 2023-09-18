from django.contrib import admin
from .models import CourseEmail, GroupEmail, ComebackJourneyEmail, ComebackWaitlistEmail



@admin.register(CourseEmail)
class CourseEmailAdmin(admin.ModelAdmin):
    list_display = ('subject','course',)
    
@admin.register(GroupEmail)
class GroupEmailAdmin(admin.ModelAdmin):
    list_display = ('subject','group',)
    list_filter = ('group',)

@admin.register(ComebackJourneyEmail)
class ComebackJourneyEmailAdmin(admin.ModelAdmin):
    list_display = ('subject','comeback',)

@admin.register(ComebackWaitlistEmail)
class ComebackWaitlistEmailAdmin(admin.ModelAdmin):
    list_display = ('subject',)

# admin.site.register(GroupEmail)