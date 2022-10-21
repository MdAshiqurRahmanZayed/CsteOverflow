from multiprocessing import context
from turtle import title
from urllib import request
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from csteusers.views import profile
from .models import Question,Comment ,teamMember,AboutPage
from .forms import *
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponseRedirect 
from django.core.paginator import Paginator, EmptyPage
from csteusers.models import Profile
from django.contrib.auth.models import User
from taggit.models import Tag 


#home
def home(request):
    about_member = teamMember.objects.all

    context={
        'about_member':about_member,

    }
    return render(request,'home.html',context)


def AllTags(request):
    tags = Tag.objects.filter().order_by('name')
    context = {
        'tags':tags 
    }
    return render(request,'cstebase/tags.html',context)
    
    

class Home(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']
    template_name = 'home.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['questions'] = context['questions'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context
    
    
    
class TagListView(ListView):
    model = Question
   
    template_name = "question_list.html"
    context_object_name = "questions"

    
    def get_queryset(self):
        return Question.objects.filter(tags__slug=self.kwargs.get('tag_slug')).order_by('-date_created')
    
# CRUD

def like_view(request, pk):
    post = get_object_or_404(Question, id=request.POST.get('question_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('cstebase:question-detail', args=[str(pk)]))

# class MyPaginator(Paginator):
#     def validate_number(self, number):
#         try:
#             return super().validate_number(number)
#         except EmptyPage:
#             if int(number) > 1:
#                 # return the last page
#                 return self.num_pages
#             elif int(number) < 1:
#                 # return the first page
#                 return 1
#             else:
#                 raise


class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']
    paginate_by = 4
    #paginator_class = MyPaginator # We use our paginator class 
    tags = Tag.objects.all 
    context ={
            'tags':tags
        }
    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     if query:
    #         object_list = self.model.objects.filter(title__icontains=query)
    #     else:
    #         object_list = self.model.objects.none()
    #     return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['questions'] = Question.objects.filter(title__icontains = search_input)
            context['search_input'] = search_input 
        # Pagination
        
        
        
        return context


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data()
        something = get_object_or_404(Question, id=self.kwargs['pk'])
        total_likes = something.total_likes()
        liked = False
        if something.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context
    

    
 


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    form_class = QuestionForm
    #fields = ['title', 'content','anonymous']

    context_object_name =  'question'
    def get_context_data(self, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all().order_by('name')
        # Add any other variables to the context here
        ...
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
    
class test(LoginRequiredMixin,CreateView):
    model = Question
    form_class = QuestionForm
    #fields = ['title', 'content','anonymous']
    template_name = "cstebase/test.html"

    context_object_name =  'question'
    def get_context_data(self, **kwargs):
        context = super(test, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all().order_by('name')
        # Add any other variables to the context here
        ...
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
   


class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Question
    #fields = ['title', 'content','anonymous']
    tags = Tag.objects.all()
    context ={
            'tags':tags
        }
    form_class = QuestionForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False


class QuestionDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Question
    context_object_name ='question'
    # template_name = "TEMPLATE_NAME"
    success_url = '/'
    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False
    

class CommentDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'cstebase/question-detail.html'
    
    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('cstebase:question-detail')

    

class AddCommentView(LoginRequiredMixin,CreateView):
    model = Comment 
    form_class = CommentForm
    
    template_name = 'cstebase/question-answer.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('cstebase:question-lists')

#Show Profile
def ShowProfile(request,str):
    #ShowProfile = Profile.objects.filter( user = str )
    ShowProfile = get_object_or_404(User,username = str )
    
    #ShowProfile = get_object_or_404(Profile,user = pk )
    context = {
    
        'ShowProfile' :ShowProfile
    }
    return render(request,'cstebase/profile_page.html',context)


# class ProfileDetailView(DetailView):
#     model = Profile
#     context_object_name = 'ShowProfile'
#     template_name = "cstebase/profile_page.html"



# def ShowAllQuestionProfileBased(request):
#     questions = Question.objects.filter(id = request.user.profile.id)
#     context = {
#         'questions':questions
#     }
#     return render(request,'cstebase/question_list.html',context)
def ShowAllQuestionProfileBased(request,str):
    questions = Question.objects.filter(user__username = str).order_by('-date_created')
    # questions = Question.objects.filter(user = str)
    paginate_by = 4
    context = {
        'questions':questions
    }
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     search_input = self.request.GET.get('search-area') or ""
    #     if search_input:
    #         context['questions'] = context['questions'].filter(title__icontains = search_input)
    #         context['search_input'] = search_input 
    
    return render(request,'cstebase/question_list_profile.html',context)


def About_page(request):
    nstu = 'About NSTU'
    vc = 'Vice Chancellor'
    about_member = teamMember.objects.all
    # about_nstu = About.objects.get()
    about_nstu = AboutPage.objects.get(title=nstu)
    about_vc = AboutPage.objects.get(title=vc)
    context={
        'about_member':about_member,
        'about_nstu':about_nstu,
        'about_vc':about_vc
    }
    
    
    return render(request,'cstebase/about.html',context)