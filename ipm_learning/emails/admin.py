from django.contrib import admin
from .models import CourseEmail, GroupEmail



@admin.register(CourseEmail)
class CourseEmailAdmin(admin.ModelAdmin):
    list_display = ('course',)
    list_filter = ('course',)
    
@admin.register(GroupEmail)
class GroupEmailAdmin(admin.ModelAdmin):
    list_display = ('group',)
    list_filter = ('group',)

# admin.site.register(GroupEmail)