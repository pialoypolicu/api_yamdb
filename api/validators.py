from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(year):
    current_year = datetime.now().date().year
    if year > current_year:
        raise ValidationError(
            _('%(value)s год введен неверно.'),
            params={'value': year},
        )
