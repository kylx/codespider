from django.db import models

class Diagnosis(models.Model):
	full_name = models.CharField(max_length=60)
	short_name = models.CharField(max_length=30, blank=True)
	def __str__(self):
		return self.full_name