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

class Watcher(models.Model):
	relationship = models.CharField(max_length=255)
	

class Building(models.Model):
	name = models.CharField(max_length=255)
	
class Room(models.Model):
	building = models.ForeignKey("Building", on_delete=models.CASCADE)
	display_name = models.CharField(max_length=20)
	capacity = models.SmallIntegerField()