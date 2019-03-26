from django.contrib import admin

from .models import Patient, Diagnosis, Watcher, Room, Building, Visit, Extension

admin.site.register(Patient)
admin.site.register(Diagnosis)	
admin.site.register(Watcher)	
admin.site.register(Room)	
admin.site.register(Building)
admin.site.register(Visit)
admin.site.register(Extension)