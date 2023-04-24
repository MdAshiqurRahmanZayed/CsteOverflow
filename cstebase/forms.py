from tkinter import Widget
from .models import Comment, Question
from django import forms 
from taggit.models import Tag 

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
        
        widgets = {
             'content' : forms.Textarea(attrs={'class':'form-control'}) ,
             
        }
class QuestionForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(label='Tags', queryset=Tag.objects.order_by('name'),widget=forms.SelectMultiple)

    class Meta:
        model = Question
        fields = ['title', 'content','anonymous',"tags"]
        
        widgets = {
             'title' : forms.TextInput(attrs={'class':'form-control '}),
             'content' : forms.Textarea(attrs={'class':'form-control'}),             
        }
