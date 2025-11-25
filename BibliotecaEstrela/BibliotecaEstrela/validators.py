from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomUserAttributeSimilarityValidator:
    message = _("Sua senha não pode ser semelhante às suas informações pessoais.")

    def validate(self, password, user=None):
        from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
        validator = UserAttributeSimilarityValidator()
        try:
            validator.validate(password, user)
        except ValidationError:
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message


class CustomMinimumLengthValidator:
    message = _("Sua senha deve ter pelo menos 8 caracteres.")

    def validate(self, password, user=None):
        from django.contrib.auth.password_validation import MinimumLengthValidator
        validator = MinimumLengthValidator(8)
        try:
            validator.validate(password, user)
        except ValidationError:
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message


class CustomCommonPasswordValidator:
    message = _("Sua senha não pode ser uma senha comum.")

    def validate(self, password, user=None):
        from django.contrib.auth.password_validation import CommonPasswordValidator
        validator = CommonPasswordValidator()
        try:
            validator.validate(password, user)
        except ValidationError:
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message


class CustomNumericPasswordValidator:
    message = _("Sua senha não pode ser inteiramente numérica.")

    def validate(self, password, user=None):
        from django.contrib.auth.password_validation import NumericPasswordValidator
        validator = NumericPasswordValidator()
        try:
            validator.validate(password, user)
        except ValidationError:
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message
