from django.db import models

		
class Visit(models.Model):
	patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
	start_date = models.DateTimeField()
	assigned_end_date = models.DateTimeField()
	actual_end_date = models.DateTimeField(null=True,blank=True)
	is_ongoing = models.NullBooleanField()
	def __str__(self):
		return self.patient