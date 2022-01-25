from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from yaml import events
from ipm_learning.content.models import Course

# Create your views here.

class HomePageView(generic.TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Course.objects.filter(
            (Q(course_type="Event") | Q(course_type="Bootcamp")) & Q(active=True)
            ).order_by('event_datetime')[:5]
        courses = Course.objects.filter(
            Q(course_type="Course") & Q(active=True)
        )[:6]
        context['next_event'] = events[:1].first()
        context['remaining_events'] = events[1:]
        context['courses'] = courses
        return context