from django.db import models

from main.enums import Enums
from .diagnosis import Diagnosis
# from .occupancy import Occupancy

class VisitManager(models.Manager):
    def get_ongoing_visit_by_patient_name(last, first, middle):
        pass
        
        
    
        
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