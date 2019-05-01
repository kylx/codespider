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
from django.urls import path, re_path, register_converter
from main.views import *

class YearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value
		
class MonthConverter:
    regex = '[0-9]{2}'

    def to_python(self, value):
        m = int(value)
        if (m == 0 or m > 12):
            raise ValueError()
		
        return m 

    def to_url(self, value):
        return '%02d' % value
        
		
register_converter(YearConverter, 'yyyy')
register_converter(MonthConverter, 'mm')

urlpatterns = [
    # main pages
	path('asd', tmp_date, name='asd'),
	re_path('asd/(?P<year>(\d{4}))/(?P<month>(\d{2}))/(?P<day>(\d{2}))', tmp_date),
	# path('asd/<yyyy:year>/<mm:month>', tmp_date),
	re_path(r'^fish$', regex, name='fish'),
	re_path(r'^fish/(?P<test>(main)|(annex))$', regex),
	
    path('home'     		, home      	, name='home'),
    path('rooms/main'    	, rooms_main     , name='rooms/main'),
    path('rooms/annex'    	, rooms_annex     , name='rooms/annex'),
    path('patients' 		, patients  , name='patients'),
    path('summary/daily'  	, summary_daily   , name='summary/daily'),
    path('summary/monthly'  , summary_monthly   , name='summary/monthly'),
    path('inquiry/filter'  	, inquiry_filter   , name='inquiry/filter'),
    path('inquiry/sort'  	, inquiry_sort   , name='inquiry/sort'),
    path('login'  			, login   , name='login'),

    # temporary
    path('tmp/create-patient', tmp_create_patient, name="forms/create-patient"),
    path('tmp/assign-room', tmp_assign_room, name="forms/assign-room"),
    path('tmp/rand', rand_patient, name="rand"),

    # requires input
    path('tmp/action/create-patient', test, name='action/create-patient'),
    path('tmp/action/assign-room', test, name='action/assign-room'),

     
    path('', show_urls, name='dev/show-urls'),

    # admin
    path('admin', admin.site.urls, name='admin'),
]
