from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    age = models.SmallIntegerField()
    sex = models.CharField(max_length=1)
 
class Diagnosis(models.Model):
	full_name = models.CharField(max_length=255)
	short_name = models.CharField(blank=True, max_length=100)
