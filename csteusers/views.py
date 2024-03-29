from ast import And
from django.shortcuts import render,redirect ,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from .models import Profile



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
        
        form = ProfileUpdateForm(request.POST or None ,  instance = obj)
       
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.success(request, f'Acount Updated Successfully!')
            return redirect('profile')
    else:

        form = ProfileUpdateForm(request.POST or None,  instance = obj)
    context = {
        'p_form': form,
        'image_form': form1,
        
    }
    return render(request, 'csteusers/profile_update.html', context)



#Email Authentications



from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from CsteOverflow import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import *
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
# from django.utils.encoding import force_text
from django.utils.encoding import force_str
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str

def signup(request):
     
     if request.method =='POST':

          email = request.POST['email']
          pass1 = request.POST['pass1']
          pass2 = request.POST['pass2']
          
          username = email.split("@")[0]
          
          
          
          if User.objects.filter(email=email).exists():
            messages.warning(request, "Email Already Registered!!")
            return redirect('signup')
       

          if pass1 != pass2:
               messages.info(request, "Passwords didn't matched!!")
               return redirect('signup')

          if not username.isalnum():
               messages.error(request, "Username must be Alpha-Numeric!!")
               return redirect('home')       
          myuser = User.objects.create_user(username, email, pass1)

          # myuser.is_active = False
          myuser.is_active = False
          myuser.save()
          messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
          
          # Welcome Email
          subject = "Welcome to CSTEOVERFLOW "
          message = "Hello " + myuser.first_name + "!! \n" + "Welcome to CSTEOVERFLOW!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address."        
          from_email = settings.EMAIL_HOST_USER
          to_list = [myuser.email]
          send_mail(subject, message, from_email, to_list, fail_silently=True)
          
          
        # Email Address Confirmation Email
          current_site = get_current_site(request)
          email_subject = "Confirm your Email @ CSTEOVERFLOW "
          message2 = render_to_string('email_confirmation.html',{
               
               'name': myuser.first_name,
               'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
               'token': generate_token.make_token(myuser)
          })
          email = EmailMessage(
               email_subject,
               message2,
               settings.EMAIL_HOST_USER,
               [myuser.email],
          )
          email.fail_silently = True
          email.send()
          
          return redirect('signin')          
            
     
     return render(request,'authentication/signup.html')

def signin(request):
     if request.method == 'POST':
          username = request.POST['username']
          pass1 = request.POST['pass1']
          
          user = authenticate(username = username,password=pass1)
          
          if user is not None:
               login(request, user)
               fname = user.first_name
               # messages.success(request, "Logged In Sucessfully!!")
               return redirect('cstebase:home')

          else:
               messages.info(request, "Bad Credentials!!")
               return redirect('signin')
               
          
     
     return render(request,'authentication/signin.html')


     
     
def activate(request,uidb64,token):
     try:
          uid = force_str(urlsafe_base64_decode(uidb64))
          myuser = User.objects.get(pk=uid)
     except(TypeError,ValueError,OverflowError,User.DoesNotExist):
          myuser = None
     
     if myuser is not None and generate_token.check_token(myuser,token):
          myuser.is_active = True
          myuser.save()
          login(request,myuser)
          return redirect('cstebase:home')
     else:
          return render(request,'activation_fails.html')
     
     
