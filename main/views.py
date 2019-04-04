from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Patient
from .enums import Enums

from django.http import HttpResponse

"""
MAIN PAGES

    frontend mag set sa final correct template
    pwede pud mag butang ug dummy context for testing

    backend mag populate sa final context
"""

def home(request):
    context = {'url_name': 'HOME'}
    return render(request, 'main/home.html', context)

def rooms(request):
    context = {'url_name': 'ROOMS'}
    return render(request, 'main/rooms.html', context)

def patients(request):
    patient_list = Patient.objects.all()
    context = {'patients': patient_list}
    return render(request, 'main/patients.html', context)

def summary(request):
    context = {'url_name': 'SUMMARY'}
    return render(request, 'main/summary.html', context)

def inquiry(request):
    context = {'url_name': 'INQUIRY'}
    return render(request, 'main/inquiry.html', context)
    
def tmp_create_patient(request):
    context = {'url_name': 'PATIENTS_CREATE'}
    return render(request, 'main/forms/patientform.html', context)

def tmp_assign_room(request):
    context = {'url_name': 'PATIENTS_CREATE'}
    return render(request, 'main/forms/roomform.html', context)

def create_patient(request):
    context = {
        'regions': Enums.REGIONS,
        'provinces': Enums.PROVINCES,
        'cities': Enums.CITIES,
    }
    return render(request, 'main/forms/patientform.html', context)


def tmp_create_patient(request):
    context = {'url_name': 'PATIENTS_CREATE'}
    return render(request, 'main/forms/patientform.html', context)

def tmp_assign_room(request):
    context = {'url_name': 'PATIENTS_CREATE'}
    return render(request, 'main/forms/roomform.html', context)

from codespider.urls import *
from django.urls import get_resolver

def show_urls(request):
    context = {
        'urls': list(get_resolver(None).reverse_dict.keys())
    }

    return render(request, 'tmp/show_urls.html', context)

def test(request):
    context = {}
    return render(request, 'tmp/todo.html', context)