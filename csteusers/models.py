from email.policy import default
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE)
     first_name = models.CharField(max_length=100,null=True,blank=True)
     last_name = models.CharField(max_length=100,null=True,blank=True)
     birthday =  models.DateField(blank=True, null=True)
     bio = models.CharField( max_length= 150)
     phone = models.IntegerField(blank=True, null=True) 
     image = models.ImageField(default ='default.jpg',  upload_to="images/profile")
     
     
     def __str__(self):
         return f'{self.user.username} - Profile'
     
     
     def save(self, *args, **kwargs):
         super().save(*args, **kwargs)
         img = Image.open(self.image.path)
         if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
     
     
     
     