from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import *
from .enums import Enums
from .forms import PatientForm, RoomForm, FilterForm
from .models import Diagnosis
import datetime

from django.http import HttpResponse

def home(request):
    context = {'url_name': 'HOME'}
    return render(request, 'main/home.html', context)

	
def rooms_main(request):
    form = RoomForm()
    occ = Occupancy.objects.filter(room__building__name="main")
    context = {
        'url_name': 'ROOMS',
		'form': form,
		'rooms': occ,
    }
    return render(request, 'main/rooms-main.html', context)
	
def rooms_annex(request):
    form = RoomForm()
    start_date = datetime.date(2019, 4, 29)
    end_date = datetime.date(2019, 4, 30)
    occ = Occupancy.objects.filter(room__building__name="annex", date__range=(start_date, end_date))
    context = {
        'url_name': 'ROOMS',
		'form': form,
		'rooms': occ,
    }
    return render(request, 'main/rooms-annex.html', context)

def patients(request):
    patient_list = Patient.objects.all()
    form = PatientForm()
    context = {
        'url_name': 'PATIENTS',
        'patients': patient_list,
		'form': form

    }
    return render(request, 'main/patients.html', context)

def summary_daily(request):
    context = {'url_name': 'SUMMARY'}
    return render(request, 'main/summary-daily.html', context)
	
def summary_monthly(request):
    context = {'url_name': 'SUMMARY'}
    return render(request, 'main/summary-monthly.html', context)

def inquiry_filter(request):
    form = FilterForm()
    context = {
        'url_name': 'INQUIRY',
        'form': form
    }
    return render(request, 'main/inquiry-filter.html', context)
	
def inquiry_sort(request):
    form = FilterForm()
    context = {
        'url_name': 'INQUIRY',
        'form': form
    }
    return render(request, 'main/inquiry-sort.html', context)
    
def tmp_create_patient(request):
    context = {'url_name': 'PATIENTS_CREATE'}
    if request.method == 'POST':
        requester = request.POST.get('diagnosis')
        post = Patient()
        post.last_name = request.POST.get('last_name')
        post.first_name = request.POST.get('first_name')
        post.middle_initial = request.POST.get('middle_initial')
        post.age = request.POST.get('age')
        post.sex = request.POST.get('sex')
        object_diagnosis = Diagnosis.objects.get(pk = requester)
        post.diagnosis = object_diagnosis
        post.region = request.POST.get('region')
        post.province = request.POST.get('province')
        post.city = request.POST.get('city')
        post.save()
        return render(request, 'main/forms/patientform.html', context)

    else:
        return render(request, 'main/forms/patientform.html', context)

def tmp_assign_room(request):
    context = {'url_name': 'PATIENTS_CREATE'}
    return render(request, 'main/forms/roomform.html', context)

def login(request):
    context = {}
    return render(request, 'main/login.html', context)
    
from django.urls import get_resolver

def show_urls(request):
    is_string   = lambda obj : isinstance(obj, str)
    is_forms    = lambda url : url.startswith('forms');
    is_action   = lambda url : url.startswith('action');
    is_dev      = lambda url : url.startswith('dev');
    is_main     = lambda url : not (is_forms(url) or is_action(url) or is_dev(url))

    # get url list, returns urlpattern strings as well as function pointers
    raw_url_list = list(get_resolver(None).reverse_dict.keys())
    # since only need urlpatterns, filter out non-strings
    url_list = list(filter(is_string, raw_url_list))

    url_main     = list(filter(is_main   , url_list))
    url_forms    = list(filter(is_forms  , url_list))
    url_actions  = list(filter(is_action , url_list))
    url_devs     = list(filter(is_dev    , url_list))

    

    context = {
        'url_list':     url_list,
        'url_main':     url_main,
        'url_forms':    url_forms,
        'url_actions':  url_actions,
        'url_devs':     url_devs,
        'raw_urls':     raw_url_list,
    }

    return render(request, 'tmp/show_urls.html', context)

def test(request):
    context = {}
    return render(request, 'tmp/todo.html', context)
from django.core import serializers
from django.http import JsonResponse
def rand_patient(request):
    data = {
        'rand_patient': serializers.serialize('json', [Patient.objects.order_by('?').first()]),
        'regions': Enums.REGIONS,
    }
    return JsonResponse(data)
	
def regex(request, test='wtf'):

	context = {
		'aaa': test,
	}
	return render(request, 'tmp/regex.html', context)
	
def tmp_date(request, year=9999, month=99, day=0):

	context = {
		'year': year,
		'month': month,
		'day': day,
	}
	return render(request, 'tmp/asd.html', context)