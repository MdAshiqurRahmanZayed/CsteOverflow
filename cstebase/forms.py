from tkinter import Widget
from .models import Comment, Question
from django import forms 

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['name','content']
        
        widgets = {
             'name' : forms.TextInput(attrs={'class':'form-control form-control form-control-lg '}),
             'content' : forms.Textarea(attrs={'class':'form-control'}) ,
             
        }
class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['title', 'content','anonymous']
        
        widgets = {
             'title' : forms.TextInput(attrs={'class':'form-control form-control form-control-lg '}),
             'content' : forms.Textarea(attrs={'class':'form-control'}),
             
        }
