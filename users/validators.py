from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    """
    Custom password validator that checks if the password contains at least one digit, 
    one lowercase letter, one uppercase letter, and one special character.
    """
    def __init__(self):
        self.password_min_length = 4
        self.password_requirements = {
            'digit': False,
            'lowercase': False,
            'uppercase': False,
            'special_char': False,
        }

    def validate(self, password, user=None):
        # Ensure password length is at least the minimum
        if len(password) < self.password_min_length:
            raise ValidationError(_('Password must be at least 4 characters long.'))

        # Check for each requirement
        for char in password:
            if char.isdigit():
                self.password_requirements['digit'] = True
            elif char.islower():
                self.password_requirements['lowercase'] = True
            elif char.isupper():
                self.password_requirements['uppercase'] = True
            elif not char.isalnum():
                self.password_requirements['special_char'] = True

        # Raise errors for any missing requirements
        for requirement, met in self.password_requirements.items():
            if not met:
                raise ValidationError(_('Password must contain at least one {}.'.format(requirement)))

    def get_help_text(self):
        return _(
            'Your password must be at least 4 characters long and contain at least one digit, '
            'one lowercase letter, one uppercase letter, and one special character.'
        )
