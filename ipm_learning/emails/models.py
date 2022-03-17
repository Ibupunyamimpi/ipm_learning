from django.db import models
from ipm_learning.content.models import Course
from django.contrib.auth.models import Group

class CourseEmail(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='emails')
    text_content = models.TextField()
    send_now = models.BooleanField(default=False)
    
    def __str__(self):
        return f"COURSE-EMAIL-{self.pk}-{self.course.name}"
    
class GroupEmail(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='emails')
    text_content = models.TextField()
    send_now = models.BooleanField(default=False)
    
    def __str__(self):
        return f"GROUP-EMAIL-{self.pk}-{self.group.name}"