import json
from dummy.management.commands._helper import *
from dummy.management.commands._visit import *
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

"""
everytime this commands is run, some fields are RE-randomized

"""





# vsisits
# for x in range(1, 20):
#     data.append(visit_start(str(x)))

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = [
            {
                "model": "auth.user",
                "pk": 1,
                "fields": {
                    "password": "pbkdf2_sha256$120000$qMvEV5wbOqE0$VCZFdXdiVBL/DfzpByAwHNvrB1hmdD1/zKQcIjlsUyg=",
                    "last_login": "2018-04-12T09:14:54.973Z",
                    "is_superuser": True,
                    "username": "test",
                    "first_name": "",
                    "last_name": "",
                    "email": "test@test.com",
                    "is_staff": True,
                    "is_active": True,
                    "date_joined": "2019-04-12T09:14:10.923Z",
                    "groups": [],
                    "user_permissions": []
                }
            },
            # diagnosis('Henlo HSA', 'HHSA'),
            # diagnosis('bagagnawowngitis', 'aa'),
            diagnosis('kulang sa gugma', 'dd'),
            diagnosis('fishisloveparinmgaulol', 'sdsd'),
            diagnosis('imong mama', 'sd'),
            diagnosis('dislocated neck', 'sd'),
            watcher('mother'),
            watcher('father'),
            watcher('grandmother'),
            watcher('grandfather'),
            # watcher('daughter'),
            # watcher('son'),
            # watcher('mistress'),
            # watcher('ex-wife'),
            # watcher('ex-husband'),
            # watcher('ex-mistress'),
            # watcher('husband'),
            # watcher('wife'),
            building('main'),
            building('annex'),
        ]
        with open('db.json', 'w') as dump_file:
            json.dump(data, dump_file, indent=4)
        call_command('loaddata', 'db.json')

        data = []

        # Add patients
        for x in range(20):
            data.append(patient())

        # Add rooms
        for x in range(0,6):
            data.append(room('main', x))
        for x in range(2,11):
            data.append(room('annex', x))
        for x in range(21,31):
            data.append(room('annex', x))

        with open('db.json', 'w') as dump_file:
            json.dump(data, dump_file, indent=4)
        call_command('loaddata', 'db.json')

        # data = []
        # for x in range(1, 20):
            # data.append(visit_start(str(x)))
        
        # with open('db.json', 'w') as dump_file:
            # json.dump(data, dump_file, indent=4)
        # call_command('loaddata', 'db.json')

        # data = []
        # for x in range(1, 200):
            # data.append(occupancy())
        # with open('db.json', 'w') as dump_file:
            # json.dump(data, dump_file, indent=4)
        # call_command('loaddata', 'db.json')
