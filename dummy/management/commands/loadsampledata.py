import json
from dummy.management.commands._helper import *
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

"""
everytime this commands is run, some fields are RE-randomized

"""


data = [
    patient('B', 'Del Campo', 20, 'm'),
    patient('B', 'Del Campo', 20, 'm'),
    patient('B', 'Del Campo', 20, 'm'),
    patient('B', 'Del Campo', 20, 'm'),
    patient('B', 'Del Campo', 20, 'm'),
    diagnosis('Henlo HSA', 'HHSA'),
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        

        with open('db.json', 'w') as dump_file:
            json.dump(data, dump_file, indent=4)

        call_command('loaddata', 'db.json')