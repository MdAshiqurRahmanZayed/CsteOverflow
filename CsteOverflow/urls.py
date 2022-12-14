"""CsteOverflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import path, include
from csteusers import views as user_view
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from cstebase import views
from csteusers.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cstebase.urls')),
    
    # Authentication System
    # path('register/',user_view.register,name='register'),
    # path('login/',auth_view.LoginView.as_view(template_name='csteusers/login.html'),name='login'),
    path('logout/',auth_view.LogoutView.as_view(template_name='csteusers/logout.html'),name='logout'),
    
    #email authentications
    path('signup/',user_view.signup,name='signup'),
    path('signin/',user_view.signin,name='signin'),
    path('activate/<uidb64>/<token>',activate,name='activate'),
    
    # Profile 
    path('profile/',user_view.profile,name= "profile" ),
    path('profile/update',user_view.profile_update,name= "profile_update" ),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('authentication/',include('csteusers.urls'))
    
    
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)