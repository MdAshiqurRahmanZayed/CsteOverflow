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
from django.db.models import Q
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
    
    
class TagListView(ListView):
    model = Question
   
    template_name = "question_list.html"
    context_object_name = "questions"

    
    def get_queryset(self):
        return Question.objects.filter(tags__slug=self.kwargs.get('tag_slug')).order_by('-date_created')
    
# CRUD

def like_view(request, pk):
    question = Question.objects.get(id = pk)
    if question.likes.filter(id = request.user.id).exists():
        question.likes.remove(request.user)
    else:
        question.likes.add(request.user)
    
    return HttpResponseRedirect(reverse('cstebase:question-detail', args=[str(pk)]))



class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']
    paginate_by = 2
    #paginator_class = MyPaginator # We use our paginator class 
    tags = Tag.objects.all 
    context ={
            'tags':tags
        }

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['questions'] = Question.objects.filter(Q(title__icontains = search_input))
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
    
def questionDetailedView(request,pk):
    question = Question.objects.get(id = pk)
    form_comment = CommentForm(request.POST or None)
    total_likes = question.likes.count()
    try:
        liked = question.likes.filter(id = request.user.id).exists()
    except:
        liked = False
    if request.method == "POST":
        if form_comment.is_valid():
            form_comment = form_comment.save(commit=False)
            form_comment.user = request.user
            form_comment.question = question
            form_comment.save()
            return redirect('cstebase:question-detail',pk)
    context={
        'question':question,
        'form_comment':form_comment,
        'total_likes':total_likes,
        'liked':liked,
    }
    return render(request,'cstebase/question_detail.html',context)

 


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    form_class = QuestionForm
    #fields = ['title', 'content','anonymous']

    context_object_name =  'question'

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
    
def answeredQuestion(request,pk1,pk):
    answered =  Comment.objects.get(id = pk)
    if answered.answered :
        answered.answered = False
    else:
        answered.answered = True
        
    answered.save()
    return redirect('cstebase:question-detail',pk1)
    


class CommentDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'cstebase/question-detail.html'
    
    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('cstebase:question-detail')

def AddCommentView(request,pk):
    question = Question.objects.get(id=pk)
    
    form  = CommentForm()
    if request.method =="POST":
        form  = CommentForm(request.POST ,request.FILES )
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.question = question
            comment.save()
            return redirect('cstebase:question-detail',pk)
        
    context = {
        "form":form
    }
    return render(request,'cstebase/question-answer.html',context)
    
def EditCommentView(request,pk,comment_id):
    comment = Comment.objects.get(id=comment_id)
    question = Question.objects.get(id=pk)
    
    
    form  = CommentForm(instance=comment)
    if request.method =="POST":
        form  = CommentForm(request.POST ,request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('cstebase:question-detail',pk)
        
    context = {
        "form":form
    }
    return render(request,'cstebase/question-answer.html',context)
   
    
def DeleteCommentView(request,pk,comment_id):
    comment = Comment.objects.get(id=comment_id)
    question = Question.objects.get(id=pk)
    if request.method =="POST":
        comment.delete()
        return redirect('cstebase:question-detail',pk)
        
    context = {
        "comment":comment,
        "question":question,
    }
    return render(request,'cstebase/question_confirm_delete.html',context)
   
    


#Show Profile
def ShowProfile(request,str):
    #ShowProfile = Profile.objects.filter( user = str )
    ShowProfile = get_object_or_404(User,username = str )
    
    #ShowProfile = get_object_or_404(Profile,user = pk )
    context = {
        'ShowProfile' :ShowProfile
    }
    return render(request,'cstebase/profile_page.html',context)



def ShowAllQuestionProfileBased(request,str):
    questions = Question.objects.filter(user__username = str).order_by('-date_created')
    # questions = Question.objects.filter(user = str)
    paginator = Paginator(questions,2)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)
    context = {
        'questions':paged_products,
        'page_obj':paged_products
    }
    return render(request,'cstebase/question_list_profile.html',context)


def About_page(request):
    nstu = 'About NSTU'
    vc = 'Vice Chancellor'
    about_member = teamMember.objects.all
    # about_nstu = About.objects.get()
    about_nstu = AboutPage.objects.get(title=nstu)
    about_vc = AboutPage.objects.get(name=vc)
    context={
        'about_member':about_member,
        'about_nstu':about_nstu,
        'about_vc':about_vc
    }
    
    
    return render(request,'cstebase/about.html',context)


def search(request):
   if 'keyword' in request.GET:
      keyword = request.GET['keyword'] 
      
      print("helllo ",keyword)
      if keyword:
         keyword = Question.objects.order_by('-date_created').filter(title__icontains=keyword)
         keyword_count = keyword.count()
         
      else:
          keyword_count = 0
         
      context = {
         'questions':keyword,
          'keyword_count':keyword_count,
      }
   return render(request,'cstebase/question_list.html',context)

