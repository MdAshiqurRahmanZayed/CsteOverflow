from tkinter import Widget
from .models import Comment, Question
from django import forms 
from taggit.models import Tag 

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['name','content']
        
        widgets = {
             'name' : forms.TextInput(attrs={'class':'form-control form-control form-control-lg '}),
             'content' : forms.Textarea(attrs={'class':'form-control'}) ,
             
        }
class QuestionForm(forms.ModelForm):
    # test = Tag.objects.order_by('name')
    # for tag in test:
    #     print(tag)
    tags = forms.ModelMultipleChoiceField(label='Tags', queryset=Tag.objects.order_by('name'),widget=forms.SelectMultiple)

    class Meta:
        model = Question
        fields = ['title', 'content','anonymous',"tags"]
        
        widgets = {
             'title' : forms.TextInput(attrs={'class':'form-control form-control form-control-lg '}),
             'content' : forms.Textarea(attrs={'class':'form-control'}),
            #  'tags' : forms.Textarea(attrs={'class':'form-control'}),
             
        }
