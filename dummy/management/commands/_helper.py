from main.enums import Enums
from main.models import Diagnosis
import random

ids = {
    'diagnosis': 1,
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

def patient(fname, mid, lname, age, sex):
    pk = ids['diagnosis']
    ids['diagnosis'] += 1

    city = random.choice(Enums.CITIES)[0]
    print(city[:2])
    print(city[:4])
    print(city[:6])

    return {
        "model": "main.patient",
        "pk": pk,
        "fields": {
            "first_name": fname,
            "last_name": lname,
            "middle_initial": mid,
            "age": age,
            "sex": sex,
            "diagnosis": Diagnosis.objects.order_by('?').first().id,
            "region": city[:2],
            "province": city[:4],
            "city": city[:6]
        }
    }