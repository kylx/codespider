from django.contrib import admin

from .models.patient import Patient
from .models.diagnosis import Diagnosis
from .models.watcher import Watcher
from .models.room import Room
from .models.building import Building
from .models.visit import Visit
from .models.extension import Extension
from .models.occupancy import Occupancy
from .models.saved_date import Saved_Date

admin.site.register(Patient)
admin.site.register(Diagnosis)	
admin.site.register(Watcher)	
admin.site.register(Room)	
# admin.site.register(Building)
# admin.site.register(Visit)
# admin.site.register(Extension)
# admin.site.register(Occupancy)
admin.site.register(Saved_Date)


admin.site.site_header = 'Admin Interface'