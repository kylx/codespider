from django import forms
from django.forms import ModelForm
from .models import Patient
from .enums import Enums
from .helpers import get_diagnosis_list
from .models import Diagnosis

class UserForm(ModelForm):
	# Temporary unless no model for form
    username = forms.CharField (
        label = 'Username',
        widget = forms.TextInput ( attrs = {
            'class' : 'input',
            'placeholder' : 'Username'
        })
    )
    
    password = forms.CharField (
        widget = forms.PasswordInput ( attrs = {
            'class' : 'input',
            'placeholder' : 'Password'
        })
    )

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'middle_initial', 'age', 'sex', 'diagnosis', 'region', 'province', 'city']
        widgets = {
            'last_name': forms.TextInput ( attrs = {
                'class' : 'input',
                'placeholder' : 'Last Name'
            }),
			
			'first_name': forms.TextInput ( attrs = {
                'class' : 'input',
                'placeholder' : 'First Name'
            }),
			
			'middle_initial': forms.TextInput ( attrs = {
                'class' : 'input',
                'placeholder' : 'Middle Initial'
            }),
			
			'age': forms.NumberInput ( attrs = {
                'class' : 'form-control, input',
			    'placeholder' : 'Age',
				'min': 0,
				'max': 100
            }),
			
			'sex': forms.Select (
			    attrs = {
				    'class' : 'form-control, input'
			    },
                choices = Enums.SEX
            ),

            'diagnosis': forms.Select (
			    attrs = {
				    'class' : 'form-control, input'
			    },
                choices = get_diagnosis_list(),
            ),
			
			'region': forms.Select (
			    attrs = {
				    'class' : 'form-control, input',
			    },
                choices = Enums.REGIONS,
            ),
			
			'province': forms.Select (
			    attrs = {
				    'class' : 'form-control, input'
			    },
                choices = Enums.PROVINCES
            ),
			
			'city': forms.Select (
			    attrs = {
				    'class' : 'form-control, input'
			    },
                choices = Enums.CITIES
            )
		}
	
class RoomForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'middle_initial']
        widgets = {
            'last_name': forms.TextInput ( attrs = {
                'class' : 'input',
                'placeholder' : 'Last Name'
            }),
			
			'first_name': forms.TextInput ( attrs = {
                'class' : 'input',
                'placeholder' : 'First Name'
            }),
			
			'middle_initial': forms.TextInput ( attrs = {
                'class' : 'input',
                'placeholder' : 'Middle Initial'
            })
		}
		
    room_num = forms.IntegerField (
		widget = forms.NumberInput ( attrs = {
            'class' : 'form-control, input',
			'placeholder' : 'Room No.',
			'min': 1
        })
    )
	
    room_num_transfer = forms.IntegerField (
        widget = forms.NumberInput ( attrs = {
            'class' : 'form-control, input',
			'placeholder' : 'Transfer to Room No.',
			'min': 1
        })
    )

    relationship = forms.MultipleChoiceField (
		widget = forms.CheckboxSelectMultiple,
		choices = [
		]
    )
	
    date_from = forms.DateField(
        widget = forms.DateInput (
			format = '%m/%d/%Y',
			attrs = {
				'type': 'date',
				'class': 'form-control'
			})
		)
    
    date_to = forms.DateField(
        widget = forms.DateInput (
			format = '%m/%d/%Y',
			attrs = {
				'type': 'date',
				'class': 'form-control'
			})
		)
	
class FilterForm(ModelForm):		
    date_from = forms.DateField (
        widget = forms.DateInput (
			format = '%m/%d/%Y',
			attrs = {
				'type': 'date',
				'class': 'form-control'
			})
		)
    
    date_to = forms.DateField(
        widget = forms.DateInput (
			format = '%m/%d/%Y',
			attrs = {
				'type': 'date',
				'class': 'form-control'
			})
		)
	
    patient = forms.MultipleChoiceField (
		widget = forms.CheckboxSelectMultiple,
		choices = [
			['p-a', 'All Patients'],
			['p-b', 'Boys'],
			['p-g', 'Girls']
		]
    )
	
    watcher = forms.MultipleChoiceField (
		widget = forms.CheckboxSelectMultiple,
		choices = [
			['w', 'Watchers'],
		]
    )
	
    building = forms.MultipleChoiceField (
		widget = forms.CheckboxSelectMultiple,
		choices = [
			['b-al', 'All Buildings'],
			['b-ma', 'Main'],
			['b-an', 'Annex'],
		]
    )
	
    class Meta:
        model = Patient
        fields = ['diagnosis', 'region', 'province', 'city']
        widgets = {
            'diagnosis': forms.Select (
			    attrs = {
				    'class' : 'form-control, input'
			    },
                choices = get_diagnosis_list(),
            ),
			
			'region': forms.Select (
			    attrs = {
				    'class' : 'form-control, input',
			    },
                choices = Enums.REGIONS,
            ),
			
			'province': forms.Select (
			    attrs = {
				    'class' : 'form-control, input'
			    },
                choices = Enums.PROVINCES
            ),
			
			'city': forms.Select (
			    attrs = {
				    'class' : 'form-control, input'
			    },
                choices = Enums.CITIES
            )
		}
		
class SummaryForm(ModelForm):
	class Meta:
		model = Patient
		fields = ['city']
		
	monthYearChosen = forms.DateField (
        widget = forms.DateInput (
			format = '%m/%Y',
			attrs = {
				'type': 'date',
				'class': 'form-control'
			})
		)