from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_initial = models.CharField(max_length=1)
    age = models.SmallIntegerField()
    sex = models.CharField(max_length=1)
    diagnosis = models.ForeignKey("Diagnosis",on_delete=models.CASCADE,null=True,blank=True)
 
class Diagnosis(models.Model):
	full_name = models.CharField(max_length=60)
	short_name = models.CharField(max_length=30, blank=True)

class Watcher(models.Model):
	relationship = models.CharField(max_length=15)
	
class Building(models.Model):
	name = models.CharField(max_length=20)
	
class Room(models.Model):
	building = models.ForeignKey("Building", on_delete=models.CASCADE)
	display_name = models.CharField(max_length=20)
	capacity = models.SmallIntegerField()
	
class Visit(models.Model):
	patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
	start_date = models.DateTimeField()
	assigned_end_date = models.DateTimeField()
	actual_end_date = models.DateTimeField()
	is_ongoing = models.NullBooleanField()
	
class Extension(models.Model):
	visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
	old_assigned_end_date = models.DateTimeField()
	
class Occupancy(models.Model):
	visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
	room = models.ForeignKey("Room", on_delete=models.CASCADE)
	watcher = models.ForeignKey("Watcher", on_delete=models.CASCADE)
	date = models.DateTimeField()