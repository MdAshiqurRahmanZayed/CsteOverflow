from re import template
from django.urls import path
from . import views



app_name = 'cstebase'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    
    
    # CRUD Function
    path('questions/',views.QuestionListView.as_view(),name='question-lists'),
    path('questions/new/',views.QuestionCreateView.as_view(),name='question-create'),
    path('questions/<int:pk>',views.QuestionDetailView.as_view(),name='question-detail'),
    path('questions/<int:pk>/update',views.QuestionUpdateView.as_view(),name='question-update'),
    path('questions/<int:pk>/delete',views.QuestionDeleteView.as_view(),name='question-delete'),
    path('questions/<int:pk>/comment',views.AddCommentView.as_view(),name='question-comment'),
    path('like/<int:pk>', views.like_view, name="like_post"),
    path('showprofile/<str:str>', views.ShowProfile,name='show_profile'),
    path('questions-all/<str:str>', views.ShowAllQuestionProfileBased,name='ShowAllQuestionProfileBased'),
    #path('all-question', views.ShowAllQuestionProfileBased, name="ShowAllQuestionProfileBased"),
    path('about/',views.About_page,name='about'),
    path('tags/<slug:tag_slug>',views.TagListView.as_view(),name="post_tag"),
    path('test/',views.test.as_view(),name="test"),
    path('tags/',views.AllTags,name="tags"),
]
    

    


