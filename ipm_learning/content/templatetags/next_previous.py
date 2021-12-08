# save under templatetags/  
from django import template

register = template.Library()


# @register.filter(name="next_item")
# def get_next(obj):
#     X = obj.__class__
#     qs =X.objects.filter(id__gt=obj.pk)
#     return qs[0].order if qs else 0

@register.filter(name="next_item")
def get_next(obj, order_by):
    X = obj.__class__
    qs = X.objects.filter(course=obj.course).filter(**{f'{order_by}__gt': getattr(obj, order_by)})
    return qs[0].get_absolute_url() if qs else 0

# @register.filter(name="previous_item")
# def get_previous(obj):
#     X = obj.__class__
#     qs = X.objects.filter(id__lt=obj.pk).order_by('-pk')
#     return qs[0] if qs else 0

@register.filter(name="previous_item")
def get_previous(obj, order_by):
    X = obj.__class__
    qs = X.objects.filter(course=obj.course).filter(**{f'{order_by}__lt': getattr(obj, order_by)}).order_by(f'-{order_by}') 
    return qs[0].get_absolute_url()  if qs else 0

"""
# for custom order_by, this would probably work: 
def get_previous(obj, order_by):
    X = obj.__class__
    qs = X.objects.filter(**{f'{order_by}__lt': getattr(obj, order_by)}).order_by(f'-{order_by}') 
    return qs[0].id if qs else 0
    
# in template:
{{ object|next_item:"sort_attribute" }}
"""