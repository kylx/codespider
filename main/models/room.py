from django.db import models

class RoomManager(models.Manager):
    def get_list(self):
        return [
            [r.pk, r.building.pk, r.display_number]
            for r in super().get_queryset()
        ]

class Room(models.Model):
    objects = RoomManager()
    building = models.ForeignKey("Building", on_delete=models.CASCADE)
    display_number = models.PositiveSmallIntegerField()
    def __str__(self):
        return f'{self.building.name} - {self.display_number}'