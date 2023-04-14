from django import template
from ipm_learning.order.models import ContentRecord, QuizRecord

register = template.Library()

@register.filter(name="filter_quiz")
def quiz_questions(user, content):
    course = content.course
    course_record = user.course_records.filter(course=course).first()
    return ContentRecord.objects.filter(content=content, course_record=course_record).first()

@register.filter(name="filter_quiz_records")
def quiz_questions(course_record):
    # course = content.course
    # course_records = user.course_records.filter(course=course).first()
    # return ContentRecord.objects.filter(content=content, course_records=course_records).first()
    return QuizRecord.objects.filter(course_record=course_record).all()

@register.filter(name="filter_quiz_question_count")
def quiz_questions(user, content):
    course = content.course
    course_records = user.course_records.filter(course=course).first()
    return ContentRecord.objects.filter(content=content, course_records=course_records).first().quiz_questions

@register.filter(name="filter_quiz_correct_ans")
def quiz_correct_ans(user, content):
    course = content.course
    course_records = user.course_records.filter(course=course).first()
    return ContentRecord.objects.filter(content=content, course_records=course_records).first().quiz_correct_ans

@register.filter(name="check_course_course_record")
def check_course_content_record(user, course):
    return user.course_records.filter(course=course).first()

# OLD WAY
@register.filter(name="content_record_complete")
def content_completer(user, content):
    course = content.course
    course_record = user.course_records.filter(course=course).first()
    return ContentRecord.objects.filter(content=content, course_record=course_record).first().complete

# NEW WAY
# @register.filter(name="content_record_complete")
# def content_completer(content):
#     content_records = getattr(content, 'user_content_records', [])
#     return content_records[0].complete if content_records else False

@register.filter(name="find_content_record_id")
def find_record_id(user, content):
    course = content.course
    course_record = user.course_records.filter(course=course).first()
    return ContentRecord.objects.filter(content=content, course_record=course_record).first().id

@register.filter(name="count_course_records")
def find_records(course_record):
    return course_record.content_records.filter(complete=True).count()

# @register.filter(name="check_course_content_record")
# def check_course_content_record(obj):
#     # course
#     X = obj.__class__
#     qs = X.objects.filter(course=obj.course).filter(**{f'{content_record_by}__gt': getattr(obj, content_record_by)})
#     return qs[0].get_absolute_url() if qs else 0