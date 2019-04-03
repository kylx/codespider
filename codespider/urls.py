"""codespider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from main.views import *
from main.models import *
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

urlpatterns = [

    path('home', home, name='home'),
    path('rooms', rooms, name='rooms'),
    path('patients', patients, name='patients'),
    path('summary', summary, name='summary'),
    path('inquiry', inquiry, name='inquiry'),
    path('tmp/create_patient', tmp_create_patient),
    path('tmp/assign_room', tmp_assign_room),

    path('admin/', admin.site.urls),
    path('create_patient', create_patient),
	path('login', login),
	path('test', test),
]
