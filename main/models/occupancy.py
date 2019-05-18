from django.db import models

import datetime

class OccupancyManager(models.Manager):
	def get_list_for_day(self, building, year, month, date):
		def simplify_occupancy(occu):
			room = occu.room
			visit = occu.visit
			patient = visit.patient
			watchers_set = occu.watcher.all().only('relationship')

			return {
				'pk': {
					'room': occu.room.pk,
					'patient': patient.pk,
					'visit': visit.pk,
				},
				'room': occu.room.display_number,
				'first_name': patient.last_name,
				'last_name': patient.first_name,
				'middle_initial': patient.middle_initial,
				'watchers': {
					'list': ', '.join([w.relationship for w in watchers_set]),
					'count': watchers_set.count(),
				},
				'date_of_stay': {
					'start': visit.start_date.strftime('%b %d'),
					'end': visit.assigned_end_date.strftime('%b %d'),
					'current': occu.date.strftime('%b %d'),
				}
			}
		start_date = datetime.date(year, month, date)
		end_date = datetime.date(year, month, date + 1)
		occ = super().select_related('room', 'visit', 'visit__patient',).prefetch_related('watcher').filter(room__building__name=building, date__range=(start_date, end_date))
		# occ = super().only(
		# 	'room',
		# 	'visit__patient__id',
		# 	'visit__patient__first_name',
		# 	'visit__patient__last_name',
		# 	'visit__patient__middle_initial',
		# 	'watcher',
		# 	'visit__id',
		# 	'visit__start_date',
		# 	'visit__assigned_end_date',
		# 	'date'
		# ).filter(room__building__name=building, date__range=(start_date, end_date))
		return list(map(simplify_occupancy, occ))


class Occupancy(models.Model):
	objects = OccupancyManager()
	visit = models.ForeignKey("Visit", on_delete=models.CASCADE)
	room = models.ForeignKey("Room", on_delete=models.CASCADE)
	watcher = models.ManyToManyField("Watcher")
	date = models.DateTimeField()

	def __str__(self):
		return f'{self.room.display_name} - {self.visit.patient.last_name}'
