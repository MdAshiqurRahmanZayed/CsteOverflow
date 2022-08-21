from turtle import title
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000,unique=True)
    content = models.TextField(null=True, blank=True)
    #likes = models.ManyToManyField(User, related_name='question_post')
    date_created = models.DateTimeField(default=timezone.now)   
    anonymous = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} - Question'
    
#     def get_absolute_url(self):
#         return reverse('stackbase:question-detail', kwargs={'pk':self.pk})
    
#     def total_likes(self):
#         return self.likes.count()