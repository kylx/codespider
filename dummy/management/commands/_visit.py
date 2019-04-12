
import random
import time
from main.models import *
from faker import Faker

ids = {
    'diagnosis': 1,
    'patient': 1,
    'watcher': 1,
    'building': 1,
    'room': 1,
    'visit': 1,
    'occupancy': 1,
    'extension': 1,
}

fake = Faker()
def get_rand_time():
    date = fake.date_time_between(start_date='-5d', end_date='now')
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')

visit_patients = {}

def visit_start(tag):
    pk = ids['visit']
    ids['visit'] += 1
    
    # get rand patient not currently visiting
    pat = Patient.objects.order_by('?').first().id

    while pat in visit_patients.values():
        pat = Patient.objects.order_by('?').first().id
        
    visit_patients[tag] = pat

    # print('hahaha', pat)
    start = get_rand_time()
    end = get_rand_time()

    return {
        'model': 'main.visit',
        'pk': pk,
        'fields': {
            'patient': pat,
            'start_date': start,
            'assigned_end_date': end,
            'actual_end_date': end,
            'is_ongoing': False,
        }
    }

def occupancy():
    pk = ids['occupancy']
    ids['occupancy'] += 1
    
    return {
        'model': 'main.occupancy',
        'pk': pk,
        'fields': {
            'visit': Visit.objects.order_by('?').first().id,
            'room': Room.objects.order_by('?').first().id,
            'watcher': [Watcher.objects.order_by('?').first().id,Watcher.objects.order_by('?').first().id,],
            'date': get_rand_time(),
        }
    }