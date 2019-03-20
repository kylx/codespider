from django.contrib import admin

from .models import Patient, Diagnosis, Watcher

admin.site.register(Patient)
admin.site.register(Diagnosis)	
admin.site.register(Watcher)	
