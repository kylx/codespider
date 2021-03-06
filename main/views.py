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
from .models.saved_date import Saved_Date
from django.utils.http import urlencode
import datetime
import json
from django.contrib import messages

from django.db.models import Q, Count

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.admin.views.decorators import staff_member_required


from django.http import HttpResponse

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
def get_today(days_delta=0):
    if Saved_Date.objects.all().count() == 0:
        date = datetime.datetime.now()
    else:
        date = Saved_Date.objects.latest('last_modified').last_modified + datetime.timedelta(days=1)
    # date = Saved_Date.objects.latest('last_modified').last_modified 
    print(f'today {date}')
    date += datetime.timedelta(days=days_delta)
    return date
    
def get_today_as_dict():
    date = get_today()
    di = {
        'year': date.year,
        'month': date.month,
        'day': date.day,
        'weekday': weekdays[date.weekday()],
        'monthname': date.strftime('%B') ,
    }
    
    print(f'ddd {di}')
    
    return di

@staff_member_required
def get_summary_monthly(request, year=-1, month=-1):
    if year == -1 or month == -1:
        date = get_today()
        year = date.year
        month = date.month
    else:
        year = int(year)
        month = int(month)
    return JsonResponse(Occupancy.objects.get_count_for_month(year, month), safe=False)

@staff_member_required
def home(request):

    year = -1
    month = -1
    day = -1

    if year == -1 and month == -1 and day == -1:
        date = get_today()
        year = date.year
        month = date.month
        day = date.day

    occ = Occupancy.objects.get_list_for_day_extended(year, month, day)
    context = {
        'today': get_today_as_dict(),
        'count': occ['count'],
        
        }
    return render(request, 'main/home.html', context)

@staff_member_required
def transfer_room(request):
    post = request.POST
    building_name = post.get('building_name', 1)
    room_number = post.get('room_num_transfer', 1)
    date = get_today()
    patient_id = post.get('transfer_patient_id', -1)
    last_name = post.get('last_name', 1)
    first_name = post.get('first_name', 1)
    middle_initial = post.get('middle_initial', 1)
    
    pat = Patient.objects.get(pk=patient_id)
    
    # check if patient exists
    # pat = Patient.objects.get_by_name(last_name, first_name, middle_initial)
    # if len(pat) == 0:
        # messages.error(request, f'Patient not found: {last_name}, {first_name} {middle_initial}.')
    # else:
        # pat = pat.first()
    
    # check if patient is currently visiting
    visit = Visit.objects.filter(patient=pat, is_ongoing=True)
    
    if len(visit) == 0:
        messages.error(request, f'ERROR: Patient {pat.last_name}, {pat.first_name} {pat.middle_initial}. is not assigned to any room.')
    else:
        
        visit = visit.first()
        # visit.is_ongoing = False
        visit.save()
    
    
    
    
        # check if room is valid
        room = Room.objects.filter(pk=room_number)[0]
        occu = Occupancy.objects.filter(
            visit=visit,
            date__date=date,
        )[0]
        if occu.room == room:
            messages.success(request, 'Transfering to the same room!')
        else:
            messages.success(request, 'Room transfer succesful!')
        occu.room = room
        occu.save()
            
        
    
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@staff_member_required
def checkout(request):
    post = request.POST
    # room_number = post.get('room_num', 1)
    patient_id = post.get('checkout_patient_id', -1)
    last_name = post.get('last_name', 1)
    first_name = post.get('first_name', 1)
    middle_initial = post.get('middle_initial', 1)
    
    pat = Patient.objects.get(pk=patient_id)
    
    # check if patient exists
    # pat = Patient.objects.get_by_name(last_name, first_name, middle_initial)
    # if len(pat) == 0:
        # messages.error(request, f'Patient not found: {last_name}, {first_name} {middle_initial}.')
    # else:
        # pat = pat.first()
        # error = f'Patient not found: {last_name}, {first_name} {middle_initial}.'
        # msg_success = f'Room assignment successful!'
    
    # check if patient is currently visiting/assigned to a room
    visit = Visit.objects.filter(patient=pat, is_ongoing=True)
    if len(visit) == 0:
        messages.error(request, f'ERROR: Patient {pat.last_name}, {pat.first_name} {pat.middle_initial}. is not assigned to any room.')
    else:
        messages.success(request, 'Checkout succesful!')
        visit = visit.first()
        visit.is_ongoing = False
        visit.actual_end_date = get_today()
        visit.save()
    context = {
        'post_stuff': post
    }
    
    
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required
def assign_room(request):
    type = 'assign room'
    error = None
    
    post = request.POST
    ll = post.getlist('id_relationship')
    building_name = post.get('building_name', 1)
    room_number = int(post.get('room_num', 1))
    last_name = post.get('last_name', 1)
    first_name = post.get('first_name', 1)
    middle_initial = post.get('middle_initial', 1)
    patient_id = post.get('assign_patient_id');
    date_to = post.get('date_to', None)
    date_from = post.get('date_from', None)
    date = post.get('date', None)
    date = get_today()
    
    msg_success = f'Room assignment successful!'
    
    
    pat = Patient.objects.get(pk=int(patient_id));
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
        # print(f"VISIT len0")
        # visit.save()
    else:
        visit = visit.first() # get first element
        visit.start_date = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        visit.assigned_end_date = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        # print(f"VISIT len0 NOT")
        
    # Get room
    room = Room.objects.filter(building__name=building_name, pk=room_number)[0]
    # print(f"ROOM {room}")
    
    occu2 = Occupancy.objects.filter(visit=visit, date=date)
    occu = Occupancy.objects.filter(visit=visit, room=room, date=date)
    is_assigned_to_same_room = len(occu) > 0
    is_already_assigned = len(occu2) > 0

    # print(f"is_assigned_to_same_room? {is_assigned_to_same_room}")
    # print(f"is_already_assigned? {is_already_assigned}")
    # print(f"today? {get_today()}")
    # print(f"date? {date}")
    
    
    if not is_assigned_to_same_room and is_already_assigned:
        occu = occu2.first()
        messages.error(request, f'ERROR: Patient already assigned at {occu.room}')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    # get list of watchers
    # i = 1
    watchers = []
    
    val = request.POST.get('rel_0', None)
    for i in range(0, int(request.POST.get('rel_count', 0))):
        val = int(request.POST.get(f'rel_{i}', None))
        watchers.append(val)
        # print(f'----------www {val} > {watchers}')
    # while val != None:
        
        
    # print(post.get(f'relationship_{i}', None))
    # for key, value in request.POST.items():
    # while post.get(f'relationship_{i}', None) is not None:
        # rel = f'relationship_{i}'
        # if key.startswith('rel_'):
            
        # rel = Watcher.objects.get(id=i).relationship
            # print(f'----------www {key} {value} = {watchers}')
            # watchers.append(int(value))
        # i += 1
    
    # watcher=Watcher.objects.order_by('?').first(),
    
    visit.save()
    if len(occu) == 0:
        occu = Occupancy(
            visit=visit,
            room=room,
            # watcher=watcher,
            date=date
            
        )
        occu.save()
        # print(f"new occu!")
    else:
        msg_success = f'Re-assigning to the same room. Old table values have been updated.'
        occu = occu.first()
        # print(f"OLD occu!")
        
    occu.watcher.clear()
    occu.watcher.set(watchers)
    # print(f'sssss {occu.watcher.all()}')
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

@staff_member_required
def rooms(request, building):
    # print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])
    form = RoomForm()

    
    date = get_today()
    year = date.year
    month = date.month
    day = date.day
    # date = datetime.datetime(int(year), int(month), int(day))
        
    

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
import json



@staff_member_required
def patients(request):
    patient_list = Patient.objects.get_list_names()
    form = PatientForm()
    context = {
        'url_name': 'PATIENTS',
        'patients': list(patient_list),
		'form': form,
        'diagnosis': Diagnosis.objects.get_diagnosis_list(),
        'patient_info': json.dumps(Patient.objects.get_history())
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

@staff_member_required
def get_filtered_patient_names(request):
    term = request.GET.get('term')
    # mid = request.GET.get('mid')
    # last = request.GET.get('last')
    return JsonResponse(Patient.objects.get_filtered_names(term), safe=False)
    
@staff_member_required
def get_filtered_relationships(request):
    term = request.GET.get('term')
    # mid = request.GET.get('mid')
    # last = request.GET.get('last')
    return JsonResponse(Watcher.objects.get_filtered_relationships(term), safe=False)

@staff_member_required
def summary_daily(request, year=-1, month=-1, day=-1):


    form = SummaryForm()
    
    if year == -1 and month == -1 and day == -1:
        # return render(request, 'main/summary-daily.html')
        date = get_today()
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
	
@staff_member_required
def summary_monthly(request):
    form = SummaryForm()
    context = {
        'url_name': 'SUMMARY',
		'form': form
    }
    return render(request, 'main/summary-monthly.html', context)

@staff_member_required
def inquiry_filter(request):
    
    print(request.GET.get('date_from'))
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    diagnosis = request.GET.get('diagnosis')
    region = request.GET.get('region')
    province = request.GET.get('province')
    city = request.GET.get('city')
    
    if date_from == '':
        date_from = None
    if date_to == '':
        date_to = None
    if diagnosis == '':
        diagnosis = None
    if region == '':
        region = None
    if province == '':
        province = None
    if city == '':
        city = None
    
    form = FilterForm()
    context = {
        'diagnosis': json.dumps(Diagnosis.objects.get_diagnosis_list()),
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
    
    if date_from == None and date_to == None and diagnosis == None and region == None and province == None and city == None:
        
        return render(request, 'main/inquiry-filter.html', context)

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
        context[building]['patients'] = sum([context[building][key] for key in ['girls', 'boys']])
        
    
        
    

    return render(request, 'main/inquiry-filter.html', context)
	
@staff_member_required
def inquiry_sort(request):
    form = FilterForm()

    # start = request.GET.get(

    print(request.GET.get('date_from'))
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    diagnosis = request.GET.get('diagnosis')
    region = request.GET.get('region')
    
    if date_from == None and date_to == None and diagnosis == None and region == None:
        context = {
            'url_name': 'INQUIRY',
            'form': form,
            'date_from': '',
            'date_to': '',
            'diagnosis': '',
            'region': '',
            'count':{
                'patients': 0,
            },
        }
    
        return render(request, 'main/inquiry-sort.html', context)
        
    
    if diagnosis == '':
        diagnosis = None
    else:
        diagnosis = Diagnosis.objects.get(pk=diagnosis);
    if region == '':
        diagnosis = None
        
    
    dd = diagnosis
    rr = region
    
    
    
    if diagnosis is None:
        dd = 'all'
    if region is None:
        rr = 'all'
    context = {
        'url_name': 'INQUIRY',
        'form': form,
        'date_from': date_from,
        'date_to': date_to,
        'diagnosis': dd,
        'region': rr,
        'count':{
            'patients': 0,
        },
        # 'diags': Patient.objects.get_diagnosis_region(1, None),
        'diags': Occupancy.objects.get_diagnosis_region(date_from, date_to, diagnosis, region),
    }
    
    filters = {}
    
    # if date_from:
        # dates_from = list(map(lambda x: int(x), date_from.split('-')))
        # dfrom = datetime.date(dates_from[0], dates_from[1], dates_from[2])
        # filters['date__date__gte']=dfrom
    # if date_to:
        # dates_to = list(map(lambda x: int(x), date_to.split('-')))
        # dto = datetime.date(dates_to[0], dates_to[1], dates_to[2])
        # filters['date__date__lte']=dto
    # if diagnosis:
        # filters['visit__patient__diagnosis']=diagnosis
    # if region:
        # filters['visit__patient__region']=region
     
    
    return render(request, 'main/inquiry-sort.html', context)
    
@staff_member_required
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
        print(post)
        
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

@staff_member_required
def tmp_assign_room(request):
    context = {'url_name': 'PATIENTS_CREATE'}
    return render(request, 'main/forms/roomform.html', context)
    
@staff_member_required
def save_day(request):
    date = get_today()
    day = Saved_Date(saved=True, last_modified=date)
    day.save()
    
    occu = Occupancy.objects.filter(date__date=date)
    for occ in occu:
        print("ASSSSASAS")
        cp = occ.copy()
        cp.date = get_today()
        cp.save()
        # watchers = occ.watcher.all()
        # occ.pk = None
        # occ.id = None
        # occ.date = get_today()
        # occ.save()
        # occ.watcher.set(watchers)
        # occ.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
	
from django.contrib.auth import logout
from django.urls import reverse
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))