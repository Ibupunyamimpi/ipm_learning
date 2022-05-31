from django.contrib import admin
from .models import Article, PageContent, PromotedCourse, TeamMember, Testimonial

# Register your models here.

admin.site.register(Article)
admin.site.register(Testimonial)
admin.site.register(TeamMember)
admin.site.register(PageContent)

@admin.register(PromotedCourse)
class PromotedCourseAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "course")