from django.db import models

from main.enums import Enums
from .diagnosis import Diagnosis

class VisitManager(models.Manager):
    def get_ongoing_visit_by_patient_name(last, first, middle):
        pass
        
        
    def get_diagnosis_region(self, start, end, diag, reg):
        
        visits = super().get_queryset().filter(start_date__lte=end, actual_end_date__gte=start)
        print(visits)
        if diag != None:
            regs = []
            visits = visits.filter(patient__diagnosis=diag)
            # visits = super().get_queryset()
            for reg in Enums.REGIONS[1:]:
                # print 
                regs.append([reg[1], visits.filter(patient__region=reg[0]).count()])
            regs.sort(key=(lambda r: r[1]), reverse=True)
            return regs
            
        if reg != None:
            diags = []
            visits = visits.filter(patient__region=reg)
            # visits = super().get_queryset()
            for diag in Diagnosis.objects.all():
                # print 
                diags.append([diag.full_name, visits.filter(patient__diagnosis=diag).count()])
            diags.sort(key=(lambda r: r[1]), reverse=True)
            return diags
            
        # if reg != None:
            # diags = []
            # pats = super().get_queryset().filter(region=reg)
            # for diag in Diagnosis.objects.all():
                # diags.append([diag.full_name, pats.filter(diagnosis=diag).count()])
            # return diags
            
        return []
        
class Visit(models.Model):
    objects = VisitManager()
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    assigned_end_date = models.DateTimeField()
    actual_end_date = models.DateTimeField(null=True,blank=True)
    is_ongoing = models.NullBooleanField()
    def __str__(self):
        return self.patient.last_name
        
    # def overlaps_date(self, start, end):
        # v = Visit.objects.filter(pk=self.pk, start_date__lte=)