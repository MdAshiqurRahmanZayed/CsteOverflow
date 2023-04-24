from turtle import title
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse 
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager



class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000,unique=True)
    content = RichTextField()
    # content = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='question_post')
    date_created = models.DateTimeField(default=timezone.now)   
    anonymous = models.BooleanField(default=False)
    # answered = models.BooleanField(default=False)
    tags = TaggableManager()
    
    
    
    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('cstebase:question-detail', kwargs={'pk':self.pk})
    
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    question = models.ForeignKey(Question,related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    date_created = models.DateTimeField(default=timezone.now)
    answered = models.BooleanField(default=False)
    
    def __str__(self):
        return f'%s - %s ' % (self.question.title,self.question.user)
    
    def get_absolute_url(self):
        return reverse('cstebase:question-detail', kwargs={'pk':self.pk})
    
    def save(self ,*args,**kwargs):
        super().save(*args,**kwargs)
        
class AboutPage(models.Model):
    name = models.CharField( max_length=50)
    title = models.CharField( max_length=50)
    about = RichTextField()
    image  = models.ImageField( upload_to='about/', height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return self.name



class teamMember(models.Model):
    name = models.CharField( max_length=50)
    title = models.CharField( max_length=50)
    about = models.TextField()
    image  = models.ImageField( upload_to='teamMember/', height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return self.name
