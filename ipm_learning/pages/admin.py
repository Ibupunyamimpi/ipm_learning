from django.contrib import admin
from .models import PageContent, TeamMember, Testimonial

# Register your models here.

admin.site.register(Testimonial)
admin.site.register(TeamMember)
admin.site.register(PageContent)