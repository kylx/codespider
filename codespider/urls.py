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
from django.urls import path, re_path, register_converter, include
from main.views import *

import debug_toolbar

urlpatterns = [
    path('debug', include(debug_toolbar.urls)),

    # main pages
    # path('asd', tmp_date, name='asd'),
    # re_path('asd/(?P<year>(\d{4}))/(?P<month>(\d{2}))/(?P<day>(\d{2}))', tmp_date),
    # path('asd/<yyyy:year>/<mm:month>', tmp_date),
    # re_path(r'^fish$', regex, name='fish'),
    # re_path(r'^fish/(?P<test>(main)|(annex))$', regex),
    
    path('home'             , home          , name='home'),
    re_path('summary/monthly/(?P<year>(\d{4}))/(?P<month>(\d{2}))', get_summary_monthly),
    re_path('rooms/(?P<building>([a-zA-Z]+))/(?P<year>(\d{4}))/(?P<month>(\d{2}))/(?P<day>(\d{2}))', rooms),
    re_path('rooms/(?P<building>([a-zA-Z]+))/(?P<year>(\d{4}))/(?P<month>(\d{2}))/(?P<day>(\d{2}))', rooms),
    re_path('rooms/(?P<building>([a-zA-Z]+))', rooms),
    path('rooms/main'        , test     , name='rooms/main'),
    path('rooms/annex'        , test     , name='rooms/annex'),
    path('patients'         , patients  , name='patients'),
    path('summary/daily'      , summary_daily   , name='summary/daily'),
    path('summary/monthly'  , summary_monthly   , name='summary/monthly'),
    path('inquiry/filter'      , inquiry_filter   , name='inquiry/filter'),
    path('inquiry/sort'      , inquiry_sort   , name='inquiry/sort'),
    path('login'              , login   , name='login'),

    # temporary
    path('tmp/create-patient', tmp_create_patient, name="forms/create-patient"),
    path('tmp/assign-room', tmp_assign_room, name="forms/assign-room"),
    path('tmp/rand', rand_patient, name="rand"),

    # requires input
    path('tmp/action/create-patient', tmp_create_patient, name='action/create-patient'),
    path('action/assign-room', assign_room, name='action/assign-room'),
    path('action/checkout', checkout, name='action/checkout'),
    path('action/transfer-room', transfer_room, name='action/transfer-room'),

    path('actions/get-filtered-patient-names', get_filtered_patient_names, name='actions/get-filtered-patient-names'),

     
    path('', show_urls, name='dev/show-urls'),

    # admin
    path('admin', admin.site.urls, name='admin'),
]
