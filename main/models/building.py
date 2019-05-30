from django.db import models

class BuildingManager(models.Manager):
    def get_list(self):
        return [[b.pk, b.name] for b in super().get_queryset()]
	
class Building(models.Model):
    objects = BuildingManager()
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name