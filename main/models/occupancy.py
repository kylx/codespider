from django.db import models

	
class Occupancy(models.Model):
	visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
	room = models.ForeignKey("Room", on_delete=models.CASCADE)
	watcher = models.ManyToManyField("Watcher")
	date = models.DateTimeField()
	def __str__(self):
		return self.visit