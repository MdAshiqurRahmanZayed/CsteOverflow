from tkinter import Widget
from .models import Comment
from django import forms 

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['name','content']
        
        widgets = {
             'name' : forms.TextInput(attrs={'class':'form-control'}),
             'content' : forms.Textarea(attrs={'class':'form-control'}) 
        }
