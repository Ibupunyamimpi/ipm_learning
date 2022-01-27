from django.contrib import admin
from .models import TeamMember, Testimonial

# Register your models here.

admin.site.register(Testimonial)
admin.site.register(TeamMember)