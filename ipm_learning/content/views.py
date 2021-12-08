from django.shortcuts import get_object_or_404, redirect, reverse
from django.views import generic
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Content, Category
from ipm_learning.order.models import Order, CourseRecord, ContentRecord, QuizRecord
from ipm_learning.order.utils import get_or_set_order_session
from ipm_learning.order.forms import AddToCartForm

import datetime

class CourseListView(generic.ListView):
    template_name = "content/course_list.html"
    queryset = Category.objects.all()
    context_object_name = "courses"

class CourseDetailView(generic.FormView):
    template_name = "content/course_detail.html"
    form_class = AddToCartForm

    def get_object(self):
        return get_object_or_404(Course, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("order:summary")

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        course = self.get_object()

        item_filter = order.order_items.filter(course=course)
        
        if not item_filter.exists():
            new_item = form.save(commit=False)
            new_item.course = course
            new_item.order = order
            new_item.save()

        return super(CourseDetailView, self).form_valid(form)

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
            quiz_record = QuizRecord.objects.get(pk=quiz_record_id)
            questions = quiz_record.content.quiz_questions.all()
            correct = 0
            for q in questions:
                if q.ans == request.POST.get(q.question):
                    correct+=1
            quiz_record.complete = True
            quiz_record.quiz_correct_ans = correct
            quiz_record.quiz_attempts += 1
            quiz_record.last_updated_on = datetime.datetime.now()
            quiz_record.save()
            course_record = quiz_record.course_record
            course_record.modules_complete = course_record.content_records.filter(complete=True).count()
            course_record.save()
            return HttpResponseRedirect(self.request.path_info)
        elif request.POST.get('record_id'):
            record_id = request.POST.get('record_id')
            record = ContentRecord.objects.get(pk=record_id)
            if not record.complete:
                record.complete = True
                record.last_updated_on = datetime.datetime.now()
                record.save()
                course_record = record.course_record
                course_record.modules_complete = course_record.content_records.filter(complete=True).count()
                course_record.save()
            content = record.content
            next_content_course_order = content.order + 1
            try:
                next_content = Content.objects.filter(course=content.course).get(order=next_content_course_order)
                return redirect(next_content)
            except:
                return HttpResponseRedirect(self.request.path_info)    
        

    def get_course(self):
        return get_object_or_404(Course, slug=self.kwargs["slug"])

    def get_object(self):
        content = get_object_or_404(Content, slug=self.kwargs["content_slug"])
        return content

    def get_queryset(self):
        course = self.get_course()
        return course.contents.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     course_record = user.course_records.filter(course=self.get_course())
    #     context.update({
    #         "course_record": course_record
    #     })
    #     return context

class CourseLibraryView(LoginRequiredMixin, generic.ListView):
    template_name = "content/course_library.html"
    context_object_name = "course_records"

    def get_queryset(self):
        user = self.request.user
        queryset = CourseRecord.objects.filter(
            user=user
        )
        return queryset
    
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