from django.db import models


class PatientsManager(models.Manager):
    def get_list_names(self):
        def simplify_patient_name(patient):
            return {
                'pk': patient.pk,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'middle_initial': patient.middle_initial,
            }
        return map(simplify_patient_name, super().get_queryset())


class Patient(models.Model):
    objects = PatientsManager()
    first_name = models.TextField()
    last_name = models.TextField()
    middle_initial = models.CharField(max_length=1)
    age = models.SmallIntegerField()
    sex = models.CharField(max_length=1)
    diagnosis = models.ForeignKey(
        "Diagnosis", on_delete=models.CASCADE, null=True, blank=True)
    region = models.CharField(max_length=6)
    province = models.CharField(max_length=6)
    city = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.last_name
