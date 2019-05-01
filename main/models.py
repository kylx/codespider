from django.db import models

class Patient(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	middle_initial = models.CharField(max_length=1)
	age = models.SmallIntegerField()
	sex = models.CharField(max_length=1)
	diagnosis = models.ForeignKey("Diagnosis",on_delete=models.CASCADE,null=True,blank=True)
	region = models.CharField(max_length=6)
	province = models.CharField(max_length=6)
	city = models.CharField(max_length=6, null=True, blank=True)
	def __str__(self):
		return self.last_name

class Diagnosis(models.Model):
	full_name = models.CharField(max_length=60)
	short_name = models.CharField(max_length=30, blank=True)
	def __str__(self):
		return self.full_name
		
class Watcher(models.Model):
	relationship = models.CharField(max_length=15)
	def __str__(self):
		return self.relationship
	
class Building(models.Model):
	name = models.CharField(max_length=20)
	def __str__(self):
		return self.name
	
class Room(models.Model):
	building = models.ForeignKey("Building", on_delete=models.CASCADE)
	display_name = models.CharField(max_length=20)
	def __str__(self):
		return self.display_name
		
class Visit(models.Model):
	patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
	assigned_end_date = models.DateTimeField()
	actual_end_date = models.DateTimeField(null=True,blank=True)
	is_ongoing = models.NullBooleanField()
	def __str__(self):
		return self.patient
	
class Extension(models.Model):
	visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
	old_assigned_end_date = models.DateTimeField()
	def __str__(self):
		return self.old_assigned_end_date
	
class Occupancy(models.Model):
	visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
	room = models.ForeignKey("Room", on_delete=models.CASCADE)
	watcher = models.ManyToManyField("Watcher")
	date = models.DateTimeField()
	def __str__(self):
		return self.visit