import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercaseValidator:
    message = _("Password must contain at least 1 uppercase letter.")
    code = "password_no_upper"

    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password or ""):
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return self.message


class LowercaseValidator:
    message = _("Password must contain at least 1 lowercase letter.")
    code = "password_no_lower"

    def validate(self, password, user=None):
        if not re.search(r"[a-z]", password or ""):
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return self.message


class NumberValidator:
    message = _("Password must contain at least 1 digit.")
    code = "password_no_number"

    def validate(self, password, user=None):
        if not re.search(r"\d", password or ""):
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return self.message


class SymbolValidator:
    message = _("Password must contain at least 1 special character: !@#$%^&*()_+-= etc.")
    code = "password_no_symbol"

    def validate(self, password, user=None):
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password or ""):
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return self.message