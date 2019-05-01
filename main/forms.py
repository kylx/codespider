from django import forms
from django.forms import ModelForm
from .models import Patient
from .enums import Enums
from .helpers import get_diagnosis_list
from .models import Diagnosis

class UserForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['username', 'password']
        
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
        fields = ['last_name', 'first_name', 'middle_initial']
        
    last_name = forms.CharField (
        label = 'Last Name',
        widget = forms.TextInput ( attrs = {
            'class' : 'input',
            'placeholder' : 'Last Name'
        })
    )
    
    first_name = forms.CharField (
        label = 'First Name',
        widget = forms.TextInput ( attrs = {
            'class' : 'input',
            'placeholder' : 'First Name'
        })
    )
    
    middle_initial = forms.CharField (
        label = 'Middle Initial',
        widget = forms.TextInput ( attrs = {
            'class' : 'input',
            'placeholder' : 'Middle Initial'
        })
    )
	
    age = forms.IntegerField (
        label = 'Age',
		widget = forms.NumberInput ( attrs = {
            'class' : 'form-control, input',
			'placeholder' : 'Age'
        })
    )
    
    sex = forms.CharField (
        label = 'Sex',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
            choices = Enums.SEX
        )
    )
    
    diagnosis = forms.CharField (
        label = 'Diagnosis',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
	         choices = get_diagnosis_list()
            # choices = DIAGNOSIS
        )
    )
    
    region = forms.CharField (
        label = 'Region',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
            
			choices = Enums.REGIONS
        )
    )
    
    province = forms.CharField (
        label = 'Province',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
		    
            choices = Enums.PROVINCES
        )
    )
    
    city = forms.CharField (
        label = 'City',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
            choices = Enums.CITIES
        )
    )
	
class RoomForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'middle_initial']
        
    last_name = forms.CharField (
        label = 'Last Name',
        widget = forms.TextInput ( attrs = {
            'class' : 'input',
            'placeholder' : 'Last Name'
        })
    )
    
    first_name = forms.CharField (
        label = 'First Name',
        widget = forms.TextInput ( attrs = {
            'class' : 'input',
            'placeholder' : 'First Name'
        })
    )
    
    middle_initial = forms.CharField (
        label = 'Middle Initial',
        widget = forms.TextInput ( attrs = {
            'class' : 'input',
            'placeholder' : 'Middle Initial'
        })
    )
	
    relationship = forms.MultipleChoiceField (
        label = 'Relationship',
		widget = forms.CheckboxSelectMultiple,
		choices = [
			['rel-1', 'Mother'],
			['rel-2', 'Father'],
		]
    )
	
    date_from = forms.DateField(
        widget=forms.DateInput( format = '%m/%d/%Y' ),
        input_formats = ( '%m/%d/%Y' )
    )
    
    date_to = forms.DateField(
        widget=forms.DateInput( format = '%m/%d/%Y' ),
        input_formats = ( '%m/%d/%Y' )
    )
	
class FilterForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['last_name', 'first_name', 'middle_initial']
		
    date_from = forms.DateField(
	widget=forms.DateInput( format = '%m/%d/%Y' ),
	input_formats = ( '%m/%d/%Y' )
    )
    
    date_to = forms.DateField(
        widget=forms.DateInput( format = '%m/%d/%Y' ),
        input_formats = ( '%m/%d/%Y' )
    )
	
    patient = forms.MultipleChoiceField (
        label = 'Relationship',
		widget = forms.CheckboxSelectMultiple,
		choices = [
			['p-a', 'All Patients'],
			['p-b', 'Boys'],
			['p-g', 'Girls']
		]
    )
	
    watcher = forms.MultipleChoiceField (
        label = 'Relationship',
		widget = forms.CheckboxSelectMultiple,
		choices = [
			['w', 'Watchers'],
		]
    )
	
    building = forms.MultipleChoiceField (
        label = 'Relationship',
		widget = forms.CheckboxSelectMultiple,
		choices = [
			['b-al', 'All Buildings'],
			['b-ma', 'Main'],
			['b-an', 'Annex'],
		]
    )
	
    diagnosis = forms.CharField (
        label = 'Diagnosis',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
		    choices = [
				['default', 'Diagnosis'],
			    ['all', 'Acute Lymphoblastic Leukemia'],
		        ['bg', 'Brainstem Glioma'],
	        ]
            # choices = DIAGNOSIS
        )
    )
    
    region = forms.CharField (
        label = 'Region',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
            choices = [
				['default', 'Region'],
			    ['r1', 'Region I (Ilocos Region)'],
		        ['r2', 'Region II (Cagayan Valley)'],
	        ]
			# choices = Enums.REGIONS
        )
    )
    
    province = forms.CharField (
        label = 'Province',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
		    choices = [
				['default', 'Province'],
			    ['r1-1', 'Ilocos Norte'],
		        ['r1-2', 'Ilocos Sur'],
	        ]
            # choices = Enums.PROVINCES
        )
    )
    
    city = forms.CharField (
        label = 'City',
        widget = forms.Select (
			attrs = {
				'class' : 'form-control, input'
			},
		    choices = [
				['default', 'City'],
			    ['r1-1-1', 'Batac'],
		        ['r1-1-2', 'Laoag'],
	        ]
            # choices = Enums.CITIES
        )
    )	