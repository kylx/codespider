from django.db import models


class Watcher(models.Model):
	relationship = models.CharField(max_length=15)
	def __str__(self):
		return self.relationship