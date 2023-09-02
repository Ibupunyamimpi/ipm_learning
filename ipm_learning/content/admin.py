from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib import admin
from .models import Course, Category, Content, Video, Event, Text, Quiz, QuizQuestion

admin.site.site_header  =  "IPM Admin"  
admin.site.site_title  =  "IPM Admin" 
admin.site.index_title  =  "IPM Admin" 

# admin.site.unregister(CourseRecord)
# admin.site.unregister(ContentRecord)
# admin.site.unregister(QuizRecord)

def activate_course(modeladmin, request, queryset):
  for course in queryset:
    course.active = True
    course.save()
activate_course.short_description = "Activate selected courses"

def deactivate_course(modeladmin, request, queryset):
  for course in queryset:
    course.active = False
    course.save()
deactivate_course.short_description = "Deactivate selected course"


admin.site.register(Category)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "course_type", "category", "price", "discount_pct", "get_discount_price", "multi_ticket", "active","is_comebackjourney")
    actions = [activate_course, deactivate_course ]
    list_filter = ('course_type', 'category', 'active', 'is_comebackjourney')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    

    # def view_content_link(self, obj):
    #     count = obj.pcontent_set.count()
    #     url = (
    #         reverse("admin:ipm_learning_course_content_changelist")
    #         + "?"
    #         + urlencode({"courses__id": f"{obj.id}"})
    #     )
    #     return format_html('<a href="{}">{} Content Blocks</a>', url, count)

    # view_content_link.short_description = "Content Blocks"

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
  def get_queryset(self, request):
        return super().get_queryset(request).select_related('course')
  list_display = ('title', 'order', 'course')
  prepopulated_fields = {
    'slug': ('title','course'), 
    }
  search_fields = ('title', 'course__name')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
  fields = ('course', 'title', 'description', 'slug', 'order', 'duration', 'forum_url', 'video_youtube_id')
  list_display = ('title', 'order', 'course')
  prepopulated_fields = {'slug': ('title',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  fields = ('course', 'title', 'description', 'slug', 'order', 'duration', 'forum_url', 'event_image', 'event_url', 'event_datetime')
  list_display = ('title', 'order', 'course')
  prepopulated_fields = {'slug': ('title',)}

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
  fields = ('course', 'title', 'description', 'slug', 'order', 'duration', 'forum_url', 'text_content')
  list_display = ('title', 'order', 'course')
  prepopulated_fields = {'slug': ('title',)}

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
  fields = ('course', 'title', 'description', 'slug', 'order', 'duration', 'forum_url')
  list_display = ('title', 'order', 'course')
  prepopulated_fields = {
    'slug': ('title','course'), 
    }

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
  list_display = ('question', 'quiz')
  list_filter = ('quiz',)

# @admin.register(CourseRecord)
# class CourseRecordAdmin(admin.ModelAdmin):
#   fields = ('user','course','paid')
#   list_display = ('course', 'user', 'created_at', 'paid')
#   list_filter = ('course', 'user', 'paid')

# @admin.register(ContentRecord)
# class ContentRecordAdmin(admin.ModelAdmin):
#   list_display = ('course_record','content', 'complete')
#   list_filter = ('course_record','content', 'complete')

# @admin.register(QuizRecord)
# class QuizRecordAdmin(admin.ModelAdmin):
#   list_display = ('course_record','content', 'complete')
#   list_filter = ('course_record','content', 'complete')