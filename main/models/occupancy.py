from django.db import models
from django.db.models import Count

from .patient import Patient
# from .building import Building
from .room import Room

import datetime
import calendar

class OccupancyManager(models.Manager):
    def get_list_for_day(self, year, month, date):
        def simplify_occupancy(occu):
            room = occu.room
            visit = occu.visit
            patient = visit.patient
            watchers_set = occu.watcher.all().only('relationship')
            start_date = visit.start_date
            end_date = visit.assigned_end_date

            return {
                'pk': {
                    'room': occu.room.pk,
                    'patient': patient.pk,
                    'visit': visit.pk,
                },
                'room': occu.room.display_number,
                'first_name': patient.last_name,
                'last_name': patient.first_name,
                'middle_initial': patient.middle_initial,
                'sex': patient.sex,
                'watchers': {
                    'list': ', '.join([w.relationship for w in watchers_set]),
                    'count': watchers_set.count(),
                },
                'date_of_stay': {
                    'start': {
                        'year': start_date.year,
                        'month': start_date.month,
                        'day': start_date.day,
                        'weekday': start_date.weekday(),
                        'month_name': start_date.strftime("%B"),
                    },
                    'end': {
                        'year': end_date.year,
                        'month': end_date.month,
                        'day': end_date.day,
                        'weekday': end_date.weekday(),
                        'month_name': end_date.strftime("%B"),
                    },
                }
            }
        start_date = datetime.date(year, month, date)
        end_date = start_date + datetime.timedelta(days=1)
        occ = super().select_related('room', 'visit', 'visit__patient',).prefetch_related('watcher').filter(visit__is_ongoing=True,room__building__name=building, date__range=(start_date, end_date)).order_by('room__display_number')
            
        llll = list(map(simplify_occupancy, occ))
        watchers = 0
        male = 0
        female = 0
        
        for o in llll:
            watchers += o['watchers']['count']
            if o['sex'] == 'm':
                male += 1
            else:
                female += 1
        return {
            'list': llll,
            'count': {
                'watchers': watchers,
                'boys': male,
                'girls': female,
                'total': male+female,
            },
            'num_rooms': Room.objects.filter(building__name=building).count()
        }
        
        
    def get_list_for_day_extended(self, year, month, date):
        def simplify_occupancy(occu):
            room = occu.room
            visit = occu.visit
            patient = visit.patient
            watchers_set = occu.watcher.all().only('relationship')
            start_date = visit.start_date
            end_date = visit.assigned_end_date
            # print(room)
            return {
                'pk': {
                    'room': occu.room.pk,
                    'patient': patient.pk,
                    'visit': visit.pk,
                },
                'room': occu.room.display_number,
                'room_name': f'{occu.room.building.name[0]}{occu.room.display_number}',
                'first_name': patient.last_name,
                'last_name': patient.first_name,
                'middle_initial': patient.middle_initial,
                'sex': patient.sex,
                'age': patient.age,
                # 'address': patient.city,
                'diagnosis': patient.diagnosis.full_name,
                'city': patient.city,
                'watchers': {
                    'list': ', '.join([w.relationship for w in watchers_set]),
                    'count': watchers_set.count(),
                },
                'date_of_stay': {
                    'start': {
                        'year': start_date.year,
                        'month': start_date.month,
                        'day': start_date.day,
                        'weekday': start_date.weekday(),
                        'month_name': start_date.strftime("%B"),
                    },
                    'end': {
                        'year': end_date.year,
                        'month': end_date.month,
                        'day': end_date.day,
                        'weekday': end_date.weekday(),
                        'month_name': end_date.strftime("%B"),
                    },
                }
            }
        start_date = datetime.date(year, month, date)
        end_date = start_date + datetime.timedelta(days=1)
        occ = super().select_related('room', 'room__building', 'visit', 'visit__patient',).prefetch_related('watcher').filter(visit__is_ongoing=True,date__range=(start_date, end_date)).order_by('room__display_number')
            
        llll = list(map(simplify_occupancy, occ))
        watchers = 0
        male = 0
        female = 0
        
        for o in llll:
            watchers += o['watchers']['count']
            if o['sex'] == 'm':
                male += 1
            else:
                female += 1
        return {
            'list': llll,
            'count': {
                'watchers': watchers,
                'boys': male,
                'girls': female,
                'total': male+female,
            },
            'num_rooms': Room.objects.all().count()
        }
    
    
    def get_count_for_date(self, year, month, day):
        date = datetime.date(year, month, day)
        query = super().get_queryset().filter(date__year=year, date__month=month, date__day=day).annotate(wcount=Count('watcher'))
        count_patients = query.count()
        count_watchers = 0
        for occ in query:
            count_watchers += occ.wcount;
            
        return {
            'patients': count_patients,
            'watchers': count_watchers,
        }
        
    def get_count_for_month(self, year, month):
        return [
            [d, Occupancy.objects.get_count_for_date(2019, 5, d)]
            for d in range(1, calendar.monthrange(year, month)[1]+1)
        ] 
        
    """
    Return status for given date and building
    If given id is null, the total is given
    
        - boys
        - girls
        - total patients
        - total watchers
    """
    def get_status_for_day(self, building_id, year, month, day):
        # prefetch fields for faster performance
        query = super().select_related('room', 'visit', 'visit__patient',).prefetch_related('watcher')
        
        query = query.filter(
            visit__is_ongoing=True,
            room__building__name=building,
            date__range=(start_date, end_date))
        query = query.order_by('room__display_number')
        
        watchers = 0
        male = 0
        female = 0
        
        for record in query:
            watcher_set = record.watcher.all().only('relationship')
            
        pass
            

class Occupancy(models.Model):
    objects = OccupancyManager()
    visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    watcher = models.ManyToManyField("Watcher")
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.room.display_number} - {self.visit.patient.last_name}'
