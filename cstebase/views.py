from urllib import request
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from .models import Question,Comment
from .forms import *
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponseRedirect
#home
def home(request):
     return render(request,'home.html')

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


class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['questions'] = context['questions'].filter(title__icontains = search_input)
            context['search_input'] = search_input
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
    fields = ['title', 'content','anonymous']
    context_object_name =  'question'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    



class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'content','anonymous']

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

    

class AddCommentView(CreateView):
    model = Comment 
    form_class = CommentForm
    
    template_name = 'cstebase/question-answer.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('cstebase:question-lists')
