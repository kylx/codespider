import json
from dummy.management.commands._helper import *
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

"""
everytime this commands is run, some fields are RE-randomized

"""


data = [
    diagnosis('Henlo HSA', 'HHSA'),
    watcher('mother'),
    watcher('father'),
    watcher('grandmother'),
    watcher('grandmother'),
    watcher('daughter'),
    watcher('son'),
    building('main'),
    building('annex'),
]

# Add patients
for x in range(100):
    data.append(patient())

# Add rooms
for x in range(1,30):
    data.append(room('main', x))
for x in range(1,25):
    data.append(room('annex', x))

class Command(BaseCommand):
    def handle(self, *args, **options):
        

        with open('db.json', 'w') as dump_file:
            json.dump(data, dump_file, indent=4)

        call_command('loaddata', 'db.json')