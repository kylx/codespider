from main.enums import Enums
from main.models import Diagnosis
from dummy.management.commands._randomdata import *
import random

ids = {
    'diagnosis': 1,
    'patient': 1,
    'watcher': 1,
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
            "diagnosis": Diagnosis.objects.order_by('?').first().id,
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