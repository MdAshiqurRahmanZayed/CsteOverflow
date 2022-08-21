from re import template
from django.urls import path
from . import views

app_name = 'cstebase'

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    
    # CRUD Function
    path('question/',views.QuestionListView.as_view(),name='question-lists'),
    path('question/<int:pk>',views.QuestionDetailView.as_view(),name='question-detail'),
    
]
