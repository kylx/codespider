from django.db import models

import datetime

class OccupancyManager(models.Manager):
	def get_list_for_day(self, building, year, month, date):
		def simplify_occupancy(occu):
			room = occu.room
			visit = occu.visit
			patient = visit.patient
			watchers_set = occu.watcher.all()

			return {
				'room': {
					'pk': occu.room.pk,
					'display_name': occu.room.display_name,
				},
				'patient': {
					'pk': patient.pk,
					# 'full_name': f'{patient.last_name}, {patient.first_name} {patient.middle_initial}.'
					'first_name': patient.last_name,
					'last_name': patient.first_name,
					'middle_initial': patient.middle_initial,
				},
				'watchers': {
					'list': ', '.join([w.relationship for w in watchers_set]),
					'count': len(watchers_set),
				},
				'date_of_stay': {
					'start': visit.start_date.strftime('%b %d'),
					'end': visit.assigned_end_date.strftime('%b %d'),
					'current': occu.date.strftime('%b %d'),
				}
			}
		start_date = datetime.date(year, month, date)
		end_date = datetime.date(year, month, date + 1)
		occ = Occupancy.objects.filter(room__building__name=building, date__range=(start_date, end_date))
		return list(map(simplify_occupancy, occ))


class Occupancy(models.Model):
	objects = OccupancyManager()
	visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
	room = models.ForeignKey("Room", on_delete=models.CASCADE)
	watcher = models.ManyToManyField("Watcher")
	date = models.DateTimeField()

	def __str__(self):
		return f'{self.room.display_name} - {self.visit.patient.last_name}'
