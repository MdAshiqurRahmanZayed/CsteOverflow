from ast import And
from django.shortcuts import render,redirect ,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from .models import Profile
# @login_required
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Successfully created for {username}! Login In Now')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'csteusers/register.html', {'form': form})

@login_required
def profile(request):
     return render(request,'csteusers/profile.html')


@login_required
def profile_update(request):
    obj = get_object_or_404(Profile, id = request.user.profile.id)
    form1 = ProfileImageForm(request.POST or None , request.FILES,  instance = obj)
    if request.method == "POST":
        #obj = get_object_or_404(Profile, id = id)
 
    # pass the object as instance in form
        # p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance = obj)
        #u_form = UserUpdateForm(request.POST, instance=request.user)
        #p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        #if u_form.is_valid() and p_form.is_valid():
        form = ProfileUpdateForm(request.POST or None ,  instance = obj)
       
        if form.is_valid() and form1.is_valid():
            #u_form.save()
            form.save()
            form1.save()
            messages.success(request, f'Acount Updated Successfully!')
            return redirect('profile')
    else:
        #u_form = UserUpdateForm(request.POST, instance=request.user)
        #p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance = request.user.profile)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        form = ProfileUpdateForm(request.POST or None,  instance = obj)
    context = {
        #'u_form': u_form,
        'p_form': form,
        'image_form': form1,
        
    }
    return render(request, 'csteusers/profile_update.html', context)

    # context ={}
 
    # obj = get_object_or_404(Profile, id = request.user.profile.id)
    # form = ProfileUpdateForm(request.POST or None, instance = obj)

    # if form.is_valid():
    #     form.save()
    #     return redirect('profile')
 
    # context["p_form"] = form
 
    # return render(request, "csteusers/profile_update.html", context) 
    


# @login_required
# class ProfileUpdateViewTest(TemplateView):
#     model = Profile
#     form_class = ProfileUpdateForm
#     #template_name = "csteusers/profile_update_test.html"





