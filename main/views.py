from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Patient

class PatientCreate(CreateView):
    model = Patient
    fields = [
		'first_name',
		'last_name',
		'middle_name',
		'age',
		'sex',
	]
	
	# first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # middle_name = models.CharField(max_length=255)
    # age = models.SmallIntegerField()
    # sex = models.CharField(max_length=1)
# Create your views here.

class PatientList(ListView):

    model = Patient
    # paginate_by = 100  # if pagination is desired

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        # return context