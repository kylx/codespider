from django.db import models

class DiagnosisManager(models.Manager):
    def get_diagnosis_list(self):
        diagnosis_qset = super().get_queryset()
        diagnoses = list(diagnosis_qset)
        diagnoses_new = []
        for i in range (len(diagnosis_qset)):
            diagnoses_new.append([
                diagnosis_qset[i].id, 
                ""+diagnosis_qset[i].full_name
            ])
        return diagnoses_new

class Diagnosis(models.Model):
    objects = DiagnosisManager()
    full_name = models.CharField(max_length=60)
    def __str__(self):
        return self.full_name
    class Meta:
         verbose_name_plural = "diagnoses"