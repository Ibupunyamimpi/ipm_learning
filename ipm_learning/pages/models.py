from django.db import models

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