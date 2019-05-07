from .models import Diagnosis


def get_diagnosis_list():
    diagnosis_qset = Diagnosis.objects.all()
    diagnoses = list(diagnosis_qset)
    diagnoses_new = []
    for i in range (len(diagnosis_qset)):
    	diagnoses_new.append((diagnosis_qset[i].id, diagnosis_qset[i].full_name))
    return diagnoses_new


def simplify_patient(patient):
    return {
        'pk': patient.pk,
        'first_name': 'OFF',
        'last_name': patient.last_name,
        'middle_initial': patient.middle_initial,
    };