from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinValueValidator, MaxValueValidator




class Category(models.Model):
    name = models.CharField(max_length=100)

    class  Meta:
        verbose_name_plural  =  "Categories" 
        
    def __str__(self):
        return self.name

class Course(models.Model):
    TYPE_CHOICES = [
    ('Course', 'Course'),
    ('Bootcamp', 'Bootcamp'),
    ('Event', 'Event'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=False,unique=True)
    course_type = models.CharField(max_length=25, choices=TYPE_CHOICES, default='Course')
    thumbnail = models.ImageField(upload_to="thumbnails/")
    description = models.TextField()
    event_datetime = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='courses')
    active = models.BooleanField(default=False)
    multi_ticket = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=0)
    discount_pct = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("content:course-detail", kwargs={"slug": self.slug})

    def get_price(self):
        return "Rp {:,}".format(self.price).replace(',','.')
    
    def get_discount_price(self):
        return "Rp {:,.0f}".format(self.price * (1 - (self.discount_pct)/100)).replace(',','.')

    def get_discount_pct(self):
        return "{0:.0%}".format(self.discount_pct/100)

class Content(models.Model):
    # Type field
    TYPE_CHOICES = [
    ('Video', 'Video'),
    ('Event', 'Event'),
    ('Text', 'Text'),
    ('Quiz', 'Quiz')
    ]
    content_type = models.CharField(max_length=25, choices=TYPE_CHOICES)

    # Common Fields
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, related_name='contents')
    title = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(null=False,unique=True)
    order = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    duration = models.CharField(max_length=100)
    forum_url = models.URLField(blank=True, null=True)

    # Video fields
    video_youtube_id = models.CharField(max_length=100, blank=True, null=True)

    # Event fields
    event_url = models.URLField(blank=True, null=True)
    event_datetime = models.DateTimeField(blank=True, null=True)
    event_image = models.ImageField(upload_to="thumbnails/", blank=True, null=True)

    # Text fields
    text_content = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["order"]
        verbose_name_plural  =  "Content Modules" 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("content:content-detail", kwargs={
            "content_slug": self.slug,
            "slug": self.course.slug,
            })


class VideoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(content_type='Video')

class Video(Content):
    objects = VideoManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        self.content_type = 'Video'
        return super(Video, self).save(*args, **kwargs)


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(content_type='Event')

class Event(Content):
    objects = EventManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        self.content_type = 'Event'
        return super(Event, self).save(*args, **kwargs)


class TextManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(content_type='Text')

class Text(Content):
    objects = TextManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        self.content_type = 'Text'
        return super(Text, self).save(*args, **kwargs)


class QuizManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(content_type='Quiz')

class Quiz(Content):
    objects = QuizManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        self.content_type = 'Quiz'
        return super(Quiz, self).save(*args, **kwargs)

    def __str__(self):
        return f"QUIZ-{self.pk}-{self.slug}-{self.course.slug}"

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.CharField(max_length=250)
    op1 = models.CharField(max_length=250)
    op2 = models.CharField(max_length=250)
    op3 = models.CharField(max_length=250)
    op4 = models.CharField(max_length=250)
    ans = models.CharField(max_length=250)
    # correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question



