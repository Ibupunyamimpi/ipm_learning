from django.db import models
from ipm_learning.content.models import Course

# Create your models here.


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile/")
    story = models.TextField()
    
    def __str__(self):
            return self.name
    

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profile/")
    story = models.TextField()
    
    def __str__(self):
            return self.name
    

class PageContent(models.Model):
    page_title = models.CharField(max_length=100)
    text_content = models.TextField()
    
    def __str__(self):
            return self.page_title
        
        
class PromotedCourse(models.Model):
    name = models.CharField(max_length=100)
    course = models.OneToOneField(Course, null=True, blank=True, on_delete=models.SET_NULL,)
    
    def __str__(self):
            return self.name
        

class Article(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="article/")
    desc = models.TextField()
    url =  models.URLField()
    
    def __str__(self):
            return self.title