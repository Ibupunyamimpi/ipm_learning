from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from ipm_learning.content.models import Course
from .models import PromotedCourse, Testimonial, TeamMember, PageContent, Article
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Create your views here.

class AboutPageView(generic.TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_content'] = PageContent.objects.get(page_title='About')
        return context


class HomePageView(generic.TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        events = Course.objects.filter(
            (Q(course_type="Event") | Q(course_type="Bootcamp")) & Q(active=True)
            ).order_by('event_datetime')[:3]
        
        # courses = Course.objects.filter(
        #     Q(course_type="Course") & Q(active=True)
        # )[:6]
        
        promo_courses = PromotedCourse.objects.all()
        
        testimonials = Testimonial.objects.all().order_by('?')[:6]
        teammembers = TeamMember.objects.all()
        articles = Article.objects.order_by().order_by('-id')[:4]
        
        context['next_event'] = events[:1].first()
        context['remaining_events'] = events[1:]
        context['courses'] = promo_courses
        context['testimonials'] = testimonials
        context['teammembers'] = teammembers
        context['articles'] = articles
        return context
    


# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID
   

def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        next = request.POST['next']

        # Communicate with Mailchimp API
        mailchimp = Client()
        mailchimp.set_config({
            "api_key": api_key,
            "server": server,
        })

        member_info = {
            "email_address": email,
            "status": "subscribed",
        }

        try:
            response = mailchimp.lists.add_list_member(list_id, member_info)
            print("response: {}".format(response))
            messages.info(request, "Sudah Berlangganan!")
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))
            messages.info(request, "Gagal Berlangganan karena format yang salah atau sudah berlangganan")

        # messages.success(request, "Email received. thank You! ")
    return redirect(next)