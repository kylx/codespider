from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_char(mi):
    if mi.isalpha():
		break
	else raise ValidationError(
            _('Invalid input'),
            params={'mi': mi},
        )