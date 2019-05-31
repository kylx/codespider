from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .enums import Enums
from .forms import PatientForm, RoomForm, FilterForm, SummaryForm
from .models.diagnosis import Diagnosis
from .models.occupancy import Occupancy
from .models.patient import Patient
from .models.visit import Visit
from .models.occupancy import Occupancy
from .models.room import Room
from .models.building import Building
from .models.watcher import Watcher
from django.utils.http import urlencode
import datetime
import json
from django.contrib import messages

from django.db.models import Q, Count

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect


from django.http import HttpResponse

def get_summary_monthly(request, year=-1, month=-1):
    if year == -1 or month == -1:
        date = datetime.datetime.now()
        year = date.year
        month = date.month
    else:
        year = int(year)
        month = int(month)
    return JsonResponse(Occupancy.objects.get_count_for_month(year, month), safe=False)

def home(request):
    context = {'url_name': 'HOME'}
    return render(request, 'main/home.html', context)

def transfer_room(request):
    post = request.POST
    building_name = post.get('building_name', 1)
    room_number = post.get('room_num_transfer', 1)
    date = post.get('date', None)
    last_name = post.get('last_name', 1)
    first_name = post.get('first_name', 1)
    middle_initial = post.get('middle_initial', 1)
    
    # check if patient exists
    pat = Patient.objects.get_by_name(last_name, first_name, middle_initial)
    if len(pat) == 0:
        messages.error(request, f'Patient not found: {last_name}, {first_name} {middle_initial}.')
    else:
        pat = pat.first()
    
        # check if patient is currently visiting
        visit = Visit.objects.filter(patient=pat, is_ongoing=True)
        
        if len(visit) == 0:
            messages.error(request, f'ERROR: Patient {last_name}, {first_name} {middle_initial}. is not assigned to any room.')
        else:
            
            visit = visit.first()
            # visit.is_ongoing = False
            visit.save()
        
        
        
        
            # check if room is valid
            room = Room.objects.filter(pk=room_number)[0]
            occu = Occupancy.objects.filter(
                visit=visit,
                date=date,
            )[0]
            if occu.room == room:
                messages.success(request, 'Transfering to the same room!')
            else:
                messages.success(request, 'Room transfer succesful!')
            occu.room = room
            occu.save()
            
        
    
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def checkout(request):
    post = request.POST
    # room_number = post.get('room_num', 1)
    last_name = post.get('last_name', 1)
    first_name = post.get('first_name', 1)
    middle_initial = post.get('middle_initial', 1)
    
    # check if patient exists
    pat = Patient.objects.get_by_name(last_name, first_name, middle_initial)
    if len(pat) == 0:
        messages.error(request, f'Patient not found: {last_name}, {first_name} {middle_initial}.')
    else:
        pat = pat.first()
        # error = f'Patient not found: {last_name}, {first_name} {middle_initial}.'
        # msg_success = f'Room assignment successful!'
    
    # check if patient is currently visiting/assigned to a room
        visit = Visit.objects.filter(patient=pat, is_ongoing=True)
        if len(visit) == 0:
            messages.error(request, f'ERROR: Patient {last_name}, {first_name} {middle_initial}. is not assigned to any room.')
        else:
            messages.success(request, 'Checkout succesful!')
            visit = visit.first()
            visit.is_ongoing = False
            visit.save()
    context = {
        'post_stuff': post
    }
    
    
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def assign_room(request):
    type = 'assign room'
    error = None
    
    post = request.POST
    ll = post.getlist('id_relationship')
    building_name = post.get('building_name', 1)
    room_number = post.get('room_num', 1)
    last_name = post.get('last_name', 1)
    first_name = post.get('first_name', 1)
    middle_initial = post.get('middle_initial', 1)
    date_to = post.get('date_to', None)
    date_from = post.get('date_from', None)
    date = post.get('date', None)
    
    msg_success = None
    
    # check if patient exists
    pat = Patient.objects.get_by_name(last_name, first_name, middle_initial)
    if len(pat) == 0:
        error = f'Patient not found: {last_name}, {first_name} {middle_initial}.'
        messages.error(request, f'Patient not found: {last_name}, {first_name} {middle_initial}.')
    else:
        # error = f'Patient not found: {last_name}, {first_name} {middle_initial}.'
        msg_success = f'Room assignment successful!'
        
        
        pat = pat[0]
    
        # check if patient is currently visiting
        visit = Visit.objects.filter(patient=pat, is_ongoing=True)
        
        # Get visit
        if len(visit) == 0:
            # create new visit if none
            visit = Visit(
                patient=pat,
                start_date=date_from,
                assigned_end_date=date_to,
                is_ongoing=True
            )
            visit.save()
        else:
            visit = visit[0] # get first element
            visit.start_date = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            print(f'date to {date_to}')
            visit.assigned_end_date = datetime.datetime.strptime(date_to, '%Y-%m-%d')
            visit.save()
        # Get room
        room = Room.objects.filter(building__name=building_name, pk=room_number)[0]
        
        # get list of watchers
        i = 1
        watchers = []
        # print(post.get(f'relationship_{i}', None))
        for key, value in request.POST.items():
        # while post.get(f'relationship_{i}', None) is not None:
            # rel = f'relationship_{i}'
            if key.startswith('relationship_'):
                
            # rel = Watcher.objects.get(id=i).relationship
                watchers.append(int(key.split('_')[1]))
            i += 1
        
        # watcher=Watcher.objects.order_by('?').first(),
        
        occu = Occupancy.objects.filter(visit=visit, room=room, date=date)
        if len(occu) == 0:
            occu = Occupancy(
                visit=visit,
                room=room,
                # watcher=watcher,
                date=date
                
            )
            occu.save()
        else:
            msg_success = f'Re-assigning to the same room. Old table values have been updated.'
            occu = occu.first()
            # occu.watcher_set.all().delete()
        
        occu.watcher.set(watchers)
        occu.save()
        
    if msg_success:
        messages.success(request, msg_success)
    
    # sum = [Occupancy.objects.get_count_for_date(2019, 5, d) for d in range(1, 32)] 
    
    context = {
        'type': type,
        'error': error,
        'watchers': sum,
        # 'post': Occupancy.objects.get_count_for_month(2019, 5),
    }
    
    
    request.session['error_msg'] = error
    request.session.modified = True
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def rooms(request, building, year=-1, month=-1, day=-1):
    # print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])
    form = RoomForm()

    if year == -1 and month == -1 and day == -1:
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
    date = datetime.datetime(int(year), int(month), int(day))
        
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # occ = Occupancy.objects.get_list_for_day(building, int(year), int(month), int(day))
    occ = Occupancy.objects.get_list_for_day(building, int(year), int(month), int(day))
    request.session['error'] = 'haha'
    context = {
        'url_name': 'ROOMS',
		'form': form,
        'building': building,
		# 'rooms': occ,
		'rooms_json': json.dumps(occ['list']),
        'year': year,
        'month': month,
        'day': day,
        'weekday': weekdays[date.weekday()],
        'month_name': date.strftime("%B"),
        'count': occ['count'],
        'relationships': Watcher.objects.get_relationship_list(),
        'rooms': Room.objects.get_list(),
        'buildings': Building.objects.get_list(),
        'num_rooms': occ['num_rooms'],
        'error': request.session.get('error_msg', 'fish'),
        
		# 'rooms': ['fish','is', 'love'],
    }
    # messages.success(request, f'ss')
    # messages.error(request, f'ee')
    return render(request, 'main/rooms.html', context)

def patients(request):
    patient_list = Patient.objects.get_list_names()
    form = PatientForm()
    context = {
        'url_name': 'PATIENTS',
        'patients': patient_list,
		'form': form,
        'diagnosis': Diagnosis.objects.get_diagnosis_list()
    }
	
	# For message after submit validation 
    # if request.method == "POST":
        # patient_form = PatientForm(request.POST)
		
        # if patient_form.is_valid():
            # patient_form.save()
            # messages.success(request, 'Patient created successfully.')
            # return render(request,"main/patients.html", context)
        # else:
            # messages.error(request, patient_form.errors)
    # messages.error(request, f'HAHAHAHA')
    # messages.success(request, f'ss')
    # messages.error(request, f'ee')
    return render(request, 'main/patients.html', context)

def get_filtered_patient_names(request):
    term = request.GET.get('term')
    # mid = request.GET.get('mid')
    # last = request.GET.get('last')
    return JsonResponse(Patient.objects.get_filtered_names(term), safe=False)

def summary_daily(request, year=-1, month=-1, day=-1):


    form = SummaryForm()
    
    if year == -1 and month == -1 and day == -1:
        # return render(request, 'main/summary-daily.html')
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
    date = datetime.datetime(int(year), int(month), int(day))
        
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # occ = Occupancy.objects.get_list_for_day(building, int(year), int(month), int(day))
    occ = Occupancy.objects.get_list_for_day_extended(int(year), int(month), int(day))
    request.session['error'] = 'haha'
    context = {
        'url_name': 'ROOMS',
		'form': form,
		# 'rooms': occ,
		'rooms_json': json.dumps(occ['list']),
        'year': year,
        'month': month,
        'day': day,
        'weekday': weekdays[date.weekday()],
        'month_name': date.strftime("%B"),
        'count': occ['count'],
        'relationships': Watcher.objects.get_relationship_list(),
        'rooms': Room.objects.get_list(),
        'buildings': Building.objects.get_list(),
        'num_rooms': occ['num_rooms'],
        'error': request.session.get('error_msg', 'fish'),
        
		# 'rooms': ['fish','is', 'love'],
    }
    # messages.success(request, f'ss')
    # messages.error(request, f'ee')
    # return render(request, 'main/rooms.html', context)
    
    # context = {
        # 'url_name': 'SUMMARY',
		# 'form': form
    # }
    return render(request, 'main/summary-daily.html', context)
	
def summary_monthly(request):
    form = SummaryForm()
    context = {
        'url_name': 'SUMMARY',
		'form': form
    }
    return render(request, 'main/summary-monthly.html', context)

def inquiry_filter(request):
    
    print(request.GET.get('date_from'))
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    diagnosis = request.GET.get('diagnosis')
    region = request.GET.get('region')
    province = request.GET.get('province')
    city = request.GET.get('city')
    
    if diagnosis == '':
        diagnosis = None
    
    form = FilterForm()
    context = {
        'url_name': 'INQUIRY',
        'form': form,
        'date_from': date_from,
        'date_to': date_to,
        'diagnosis': diagnosis,
        'region': region,
        'province': province,
        'city': city,
        'both': {
            'patients': 0,
            'boys': 0,
            'girls': 0,
            'watchers': 0,
        
        },
        'main': {
            'patients': 0,
            'boys': 0,
            'girls': 0,
            'watchers': 0,
        },
        'annex': {
            'patients': 0,
            'boys': 0,
            'girls': 0,
            'watchers': 0,
        },
    }
    
    filters = {}
    
    if date_from:
        dates_from = list(map(lambda x: int(x), date_from.split('-')))
        dfrom = datetime.date(dates_from[0], dates_from[1], dates_from[2])
        filters['date__date__gte']=dfrom
    if date_to:
        dates_to = list(map(lambda x: int(x), date_to.split('-')))
        dto = datetime.date(dates_to[0], dates_to[1], dates_to[2])
        filters['date__date__lte']=dto
    if diagnosis:
        filters['visit__patient__diagnosis']=diagnosis
    if region:
        filters['visit__patient__region']=region
    if province:
        filters['visit__patient__province']=province
    if city:
        filters['visit__patient__city']=city

    
    # date = Q(date__gte=date_from, date__lte=date_to)
    
    # dates_to = list(map(lambda x: int(x), date_to.split('-')))
    
    # dto = datetime.date(dates_to[0], dates_to[1], dates_to[2])
    # print(f'{dfrom}   {dto}')
    records = Occupancy.objects.filter(**filters).annotate(wcount=Count('watcher'))
    for rec in records:
        if rec.visit.patient.sex == 'm':
            sex = 'boys'
        else:
            sex = 'girls'
            
        context[rec.room.building.name][sex] += 1
        context[rec.room.building.name]['watchers'] += rec.wcount
        context['both'][sex] += 1
        context['both']['watchers'] += rec.wcount
    
    for building in ['both', 'main', 'annex']:
        context[building]['patients'] = sum([context[building][key] for key in ['girls', 'boys', 'watchers']])
        
    
        
    

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
        
        if len(Patient.objects.filter(first_name= post.first_name,middle_initial= post.middle_initial,last_name=post.last_name)) == 0:
            post.save()
            messages.success(request, f'Patient creation successful')
        else:
            messages.error(request, f'ERROR: Patient {post.last_name}, {post.first_name} {post.middle_initial}. already exists')
        # return render(request, 'main/forms/patientform.html', context)

    # else:
    # messages.error(request, f'a{post.last_name}')
    # messages.error(request, f'b{post.first_name}')
    # messages.error(request, f'c{post.middle_initial}')
    return redirect('patients')

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