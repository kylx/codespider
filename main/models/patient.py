from django.db import models

from .diagnosis import Diagnosis
from main.enums import Enums
from .visit import Visit
from .occupancy import Occupancy

def simplify_patient_name(patient):
    return {
        'pk': patient.pk,
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'middle_initial': patient.middle_initial,
    }
    
def simplify_patient_extended(patient):
    return {
        'pk': patient.pk,
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'middle_initial': patient.middle_initial,
    }

class PatientsManager(models.Manager):
    def get_list_names(self):
        return map(simplify_patient_name, super().get_queryset())
    
    def get_by_name(self, last, first, mid):
        # super().get_queryset()  <---- get all patients
        return super().get_queryset().filter(last_name=last, first_name=first, middle_initial=mid)

    def get_filtered_names(self, term):
        # filters = {}
        # if first:
        #     filters['first_name__icontains'] = first
        # if mid:
        #     filters['middle_initial__iexact'] = mid
        # if last:
        #     filters['last_name__icontains'] = last
        query = super().get_queryset().filter(
            models.Q(first_name__icontains=term) |
            models.Q(middle_initial__iexact=term) |
            models.Q(last_name__icontains=term)
            )


        return list(map(simplify_patient_name, query))
        
    def get_diagnosis_region(self, start, end, diag, reg):
        
        # if diag != None:
            # regs = []
            # visits = Visit.objects.filter(diagnosis=diag)
            # for reg in Enums.REGIONS[1:]:
                # print 
                # regs.append([reg[1], pats.filter(region=reg[0]).count()])
            # return regs
            
        # if reg != None:
            # diags = []
            # pats = super().get_queryset().filter(region=reg)
            # for diag in Diagnosis.objects.all():
                # diags.append([diag.full_name, pats.filter(diagnosis=diag).count()])
            # return diags
            
        return []
        
    def get_history(self):
        pats = []
        for pat in super().get_queryset().all():
            
            code = pat.city
            reg = [x[1] for x in Enums.REGIONS if x[0] == code[0:2]][0]
            if reg.startswith('r'):
                reg = reg.split('-')[1].strip()
            else:
                reg = reg.split('-')[0].strip()
            prov = [x[1] for x in Enums.PROVINCES if x[0] == code[0:4]][0]
            city = [x[1] for x in Enums.CITIES if x[0] == code[0:6]][0]
        
            pats.append({
                'first_name': pat.first_name,
                'last_name': pat.last_name,
                'middle_initial': pat.middle_initial,
                'age': pat.age,
                'sex': pat.sex,
                'region': reg,
                'diagnosis': pat.diagnosis.full_name,
                'province': prov,
                'city': city,
                'total_days': Visit.objects.filter(patient=pat).count(),
                'frequency': Occupancy.objects.filter(visit__patient=pat).count(),
                'dates_of_stay': [
                    {'from': x.start_date.strftime('%Y-%m-%d'), 
                    'to': x.assigned_end_date.strftime('%Y-%m-%d')}
                    for x in Visit.objects.filter(patient=pat)],
            
            })
        return pats
                

class Patient(models.Model):
    objects = PatientsManager()
    first_name = models.TextField()
    last_name = models.TextField()
    middle_initial = models.CharField(max_length=1)
    age = models.SmallIntegerField()
    sex = models.CharField(max_length=1)
    diagnosis = models.ForeignKey("Diagnosis",on_delete=models.CASCADE,null=True,blank=True)
    region = models.CharField(max_length=6)
    province = models.CharField(max_length=6)
    city = models.CharField(max_length=6, null=True, blank=True)
    def __str__(self):
        return self.last_name