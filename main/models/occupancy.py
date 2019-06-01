from django.db import models
from django.db.models import Count, Q

from .patient import Patient
# from .building import Building
from .room import Room
from .visit import Visit
from .diagnosis import Diagnosis
from main.enums import Enums

import datetime
import calendar

class OccupancyManager(models.Manager):
    def get_list_for_day(self, building, year, month, date):
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
            
            
            code = patient.city
            
            
            
            reg = [x[1] for x in Enums.REGIONS if x[0] == code[0:2]][0]
            if reg.startswith('r'):
                reg = reg.split('-')[1].strip()
            else:
                reg = reg.split('-')[0].strip()
            prov = [x[1] for x in Enums.PROVINCES if x[0] == code[0:4]][0]
            city = [x[1] for x in Enums.CITIES if x[0] == code[0:6]][0]
            
            # print(room)
            return {
                'pk': {
                    'room': occu.room.pk,
                    'patient': patient.pk,
                    'visit': visit.pk,
                },
                'room': occu.room.display_number,
                'room_name': f'{occu.room.building.name[0].upper()}{occu.room.display_number}',
                'first_name': patient.last_name,
                'last_name': patient.first_name,
                'middle_initial': patient.middle_initial,
                'sex': patient.sex.upper(),
                'age': patient.age,
                # 'address': patient.city,
                'diagnosis': patient.diagnosis.full_name,
                'city': f'{reg}, {prov.title()}, {city.title()}',
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
        occ = super().select_related('room', 'room__building', 'visit', 'visit__patient',).prefetch_related('watcher').filter(visit__is_ongoing=True,date__range=(start_date, end_date)).order_by('-room__building__name', 'room__display_number')
            
        llll = list(map(simplify_occupancy, occ))
        watchers = 0
        male = 0
        female = 0
        
        for o in llll:
            watchers += o['watchers']['count']
            if o['sex'] == 'M':
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
        count_patients = 0
        count_watchers = 0
        start = datetime.date(year, month, day)
        end = start + datetime.timedelta(days=1)
        occu = Occupancy.objects.filter(date__lte=end, date__gte=start).annotate(wcount=Count('watcher'))
        # for visit in visits:
            # occu = visit.occupancy_set.filter(date__gte=start, date__lte=end)
            # count_patients += occu.count()
            # for occ in occu:
                # count_watchers += occ.watcher.all().count()
        # query = super().get_queryset().filter(date__gte=start, date__lte=end).annotate(wcount=Count('watcher'))
        count_patients = occu.count()
        for occ in occu:
            count_watchers += occ.wcount;
            
        return {
            'patients': count_patients,
            'watchers': count_watchers,
        }
        
    def get_count_for_month(self, year, month):
        return [
            [d, Occupancy.objects.get_count_for_date(year, month, d)]
            for d in range(1, calendar.monthrange(year, month)[1]+1)
        ] 
        
    def get_diagnosis_region(self, start, end, diag, reg):
        
        visits = super().get_queryset().filter(date__lte=end, date__gte=start)
        print(visits)
        if diag != None:
            regs = []
            visits = visits.filter(visit__patient__diagnosis=diag)
            # visits = super().get_queryset()
            for reg in Enums.REGIONS[1:]:
                # print 
                regs.append([reg[1], visits.filter(visit__patient__region=reg[0]).count()])
            regs.sort(key=(lambda r: r[1]), reverse=True)
            return regs
            
        if reg != None:
            diags = []
            visits = visits.filter(visit__patient__region=reg)
            # visits = super().get_queryset()
            for diag in Diagnosis.objects.all():
                # print 
                diags.append([diag.full_name, visits.filter(visit__patient__diagnosis=diag).count()])
            diags.sort(key=(lambda r: r[1]), reverse=True)
            return diags
            
        # if reg != None:
            # diags = []
            # pats = super().get_queryset().filter(region=reg)
            # for diag in Diagnosis.objects.all():
                # diags.append([diag.full_name, pats.filter(diagnosis=diag).count()])
            # return diags
            
        return []
        
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
