from django.contrib import admin

from .models import Patient, Diagnosis

admin.site.register(Patient)
admin.site.register(Diagnosis)	
