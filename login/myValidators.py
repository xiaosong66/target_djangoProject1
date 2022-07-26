from django.conf import settings
from django.core.cache import cache

from .auth_password_validators import ComplexityValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Settings
PASSWORD_COMPLEXITY = getattr(settings, "PASSWORD_COMPLEXITY", None)


# 验证密码强度
def pdComplexityValidator(password):
    myValidator = ComplexityValidator(password, PASSWORD_COMPLEXITY)
    myValidator()


def judgeRegistered(username):
    code = "userExistError"

    obj = User.objects.filter(username=username).first()
    if obj is not None:
        raise ValidationError(_("%(username)s用户已存在"),
                              params={'username': username},
                              code=code)


def verifyCode(code):
    rightCode = cache.get("verifyCode")
    if rightCode != code:
        raise ValidationError(_("验证码错误"))
