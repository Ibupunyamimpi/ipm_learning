from django.contrib import admin
from .models import PageContent, PromotedCourse, TeamMember, Testimonial

# Register your models here.

admin.site.register(Testimonial)
admin.site.register(TeamMember)
admin.site.register(PageContent)
admin.site.register(PromotedCourse)