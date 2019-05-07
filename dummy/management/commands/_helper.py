from main.enums import Enums
from main.models.diagnosis import Diagnosis
from main.models.patient import Patient
from main.models.building import Building
from main.models.room import Room
from dummy.management.commands._randomdata import *
import random

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

def diagnosis(full_name, short_name=None):
    pk = ids['diagnosis']
    ids['diagnosis'] += 1
    return {
        'model': 'main.diagnosis',
        'pk': pk,
        'fields':{
            'full_name': full_name,
            'short_name': short_name,
        },
    }

def patient():
    pk = ids['patient']
    ids['patient'] += 1

    city = random.choice(Enums.CITIES)[0]

    fname = random.choice(fnames)
    rr = random.random()
    if (rr < 0.7):
        fname += ' ' + random.choice(fnames)
    elif (random.random() < 0.1):
        fname += ' ' + random.choice(fnames)
    return {
        "model": "main.patient",
        "pk": pk,
        "fields": {
            "first_name": fname,
            "last_name": random.choice(lnames),
            "middle_initial": random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            "age": random.choice(range(5,20)),
            "sex": random.choice('mf'),
            "diagnosis": random.choice(range(1, ids['diagnosis'])),
            "region": city[:2],
            "province": city[:4],
            "city": city[:6]
        }
    }

def watcher(rel):
    pk = ids['watcher']
    ids['watcher'] += 1

    return {
        "model": "main.watcher",
        "pk": pk,
        "fields": {
            "relationship": rel,
        }
    }

def building(name):
    pk = ids['building']
    ids['building'] += 1

    return {
        "model": "main.building",
        "pk": pk,
        "fields": {
            "name": name,
        }
    }

def room(building, num):
    pk = ids['room']
    ids['room'] += 1

    return {
        "model": "main.room",
        "pk": pk,
        "fields": {
            'building': Building.objects.get(name=building).id,
            "display_name": 'Room ' + str(num),
        }
    }

