from django.shortcuts import get_object_or_404, redirect, reverse
from django.views import generic
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Course, Content, Category
from ipm_learning.order.models import Order, CourseRecord, ContentRecord, QuizRecord, OrderItem
from ipm_learning.order.utils import get_or_set_order_session
from ipm_learning.order.forms import AddToCartForm
from ipm_learning.comeback.models import ComebackRecord
from django.contrib import messages
from django.db.models import Prefetch, F



import datetime

# class CourseListView(generic.ListView):
#     template_name = "content/course_list.html"
#     queryset = Category.objects.all()
#     context_object_name = "courses"
    
class EventListView(generic.ListView):
    template_name = "content/event_list.html"
    queryset = Course.objects.filter(
        (Q(course_type="Event") | Q(course_type="Bootcamp")) & Q(active=True)
    ).order_by('event_datetime')
    context_object_name = "events"  

class CourseListView(generic.ListView):
    template_name = "content/course_list.html"
    queryset = Category.objects.all()
    context_object_name = "courses"

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['events'] = Course.objects.filter(
            (Q(course_type="Event") | Q(course_type="Bootcamp")) & Q(active=True)
        ).order_by('event_datetime')
        return context

class CourseDetailView(generic.FormView):
    template_name = "content/course_detail.html"
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Course, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("order:summary")

    # def form_valid(self, form):
    #     order = get_or_set_order_session(self.request)
    #     course = self.get_object()

    #     item_filter = order.order_items.filter(course=course)
        
    #     if not item_filter.exists():
    #         new_item = form.save(commit=False)
    #         new_item.course = course
    #         new_item.order = order
    #         new_item.save()

    #     return super(CourseDetailView, self).form_valid(form)
    
    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(self.request)
        course = self.get_object()
        
        if not request.user.is_authenticated:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            if request.POST.get('quantity'):
                quantity= request.POST.get('quantity')
            else:
                quantity = 1
            item_filter_lst = order.order_items.filter(course=course)
            
            if not item_filter_lst.exists():
                new_item = OrderItem.objects.create(
                    course = course,
                    order = order,
                    tickets = quantity,
                )
                new_item.save()
                return redirect("order:summary")
            elif course.multi_ticket:
                current_item = order.order_items.get(course=course)
                current_item.tickets = quantity
                current_item.save()
                return redirect("order:summary")
            else:
                messages.info(self.request, "This item is already in your cart")
                return redirect("order:summary") 
            
    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['course'] = self.get_object()
        return context


# class CourseDetailView(generic.DetailView):
#     template_name = "content/course_detail.html"
#     queryset = Course.objects.all()
#     context_object_name = "course"

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#         course_id = request.POST.get('course_id')
#         course = Course.objects.get(pk=course_id)
#         course_record = CourseRecord(course=course, user=self.request.user)
#         course_record.save()
#         return redirect(course.contents.first())


class ContentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "content/content_detail.html"

    def post(self, request, *args, **kwargs):
        if request.POST.get('quiz_record_id'):
            quiz_record_id = request.POST.get('quiz_record_id')
            
            # Optimize quiz_record update
            questions = QuizRecord.objects.get(pk=quiz_record_id).content.quiz_questions.all()
            correct = sum([q.ans == request.POST.get(q.question) for q in questions])
            QuizRecord.objects.filter(pk=quiz_record_id).update(
                complete=True,
                quiz_correct_ans=correct,
                quiz_attempts=F('quiz_attempts')+1,
                last_updated_on=datetime.datetime.now()
            )
            
            # quiz_record = QuizRecord.objects.get(pk=quiz_record_id)
            # questions = quiz_record.content.quiz_questions.all()
            # correct = 0
            # for q in questions:
            #     if q.ans == request.POST.get(q.question):
            #         correct+=1
            # quiz_record.complete = True
            # quiz_record.quiz_correct_ans = correct
            # quiz_record.quiz_attempts += 1
            # quiz_record.last_updated_on = datetime.datetime.now()
            # quiz_record.save()
            
            # Optimize course_record update
            course_record_id = QuizRecord.objects.get(pk=quiz_record_id).course_record.id
            modules_complete = ContentRecord.objects.filter(course_record_id=course_record_id, complete=True).count()
            CourseRecord.objects.filter(pk=course_record_id).update(modules_complete=modules_complete)
            
            # course_record = quiz_record.course_record
            # course_record.modules_complete = course_record.content_records.filter(complete=True).count()
            # course_record.save()
            
        elif request.POST.get('record_id'):
            record_id = request.POST.get('record_id')
            ContentRecord.objects.filter(pk=record_id, complete=False).update(
                complete=True,
                last_updated_on=datetime.datetime.now()
            )

            # Optimize course_record update
            course_record_id = ContentRecord.objects.get(pk=record_id).course_record.id
            modules_complete = ContentRecord.objects.filter(course_record_id=course_record_id, complete=True).count()
            CourseRecord.objects.filter(pk=course_record_id).update(modules_complete=modules_complete)

            # record_id = request.POST.get('record_id')
            # record = ContentRecord.objects.get(pk=record_id)
            # if not record.complete:
            #     record.complete = True
            #     record.last_updated_on = datetime.datetime.now()
            #     record.save()
            #     course_record = record.course_record
            #     course_record.modules_complete = course_record.content_records.filter(complete=True).count()
            #     course_record.save()
            # content = record.content
            
            content = ContentRecord.objects.get(pk=record_id).content
            next_content_course_order = content.order + 1
            try:
                next_content = Content.objects.filter(course=content.course).get(order=next_content_course_order)
                return redirect(next_content)
            except Content.DoesNotExist:
                return HttpResponseRedirect(self.request.path_info)
        
        return HttpResponseRedirect(self.request.path_info)    

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs["slug"])

    def get_object(self):
        content = get_object_or_404(Content, slug=self.kwargs["content_slug"])
        return content

    # def get_queryset(self):
    #     # OLD WAY
    #     # course = self.get_course()
        
    #     # NEW WAY
    #     course = Course.objects.prefetch_related(
    #         Prefetch(
    #             'contents__content_records',
    #             queryset=ContentRecord.objects.filter(course_record__user=self.request.user),
    #             to_attr='user_content_records'
    #         )
    #     ).get(slug=self.kwargs["slug"])
        
    #     return course.contents.prefetch_related('course__contents').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the course by slug
        course = Course.objects.get(slug=self.kwargs["slug"])

        # Fetch related contents
        contents = course.contents.all()

        # Fetch content records for this course and user
        content_records = ContentRecord.objects.filter(
            course_record__course=course,
            course_record__user=self.request.user
        )
        context['contents'] = contents
        context['content_records'] = content_records
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     course_record = user.course_records.filter(course=self.get_course())
    #     context.update({
    #         "course_record": course_record
    #     })
    #     return context

# class CourseLibraryView(LoginRequiredMixin, generic.ListView):
#     template_name = "content/course_library.html"
#     context_object_name = "course_records"

#     def get_queryset(self):
#         user = self.request.user
#         queryset = CourseRecord.objects.filter(
#             user=user
#         )
#         return queryset
    
class CourseLibraryView(LoginRequiredMixin, generic.ListView):
        template_name = "content/course_library.html"
        context_object_name = "course_records"

        def get_queryset(self):
            user = self.request.user
            
            # Query for CourseRecords associated with the user 
            # and where course.is_comebackjourney is False
            queryset = CourseRecord.objects.filter(
                user=user,
                course__is_comebackjourney=False
            )
            
            return queryset

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            user = self.request.user
            
            # Get today's date
            today = timezone.now().date()
            
            # Query for ComebackRecords where is_active is True
            comeback_records = ComebackRecord.objects.filter(
                user=user,
                is_active=True
            )
            
            # Determine if the Comeback Journey is live
            for record in comeback_records:
                record.is_live = record.comeback.course_start_date <= today
            
            # Add the comeback_records queryset to the context with the is_live attribute
            context['comeback_records'] = comeback_records

            return context
        
        
        
        
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     user = self.request.user
    #     user.course_records.
    #     if user.is_organizer:
    #         queryset = Lead.objects.filter(
    #             organization=user.userprofile,
    #             agent__isnull=True
    #         )

    #     context.update({
    #         "unassigned_leads": queryset
    #     })
    #     return context