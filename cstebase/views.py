from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Question
#home
def home(request):
     return render(request,'home.html')
#about
def about(request):
     return render(request,'about.html')



# CRUD


class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']

class QuestionDetailView(DetailView):
    model = Question
