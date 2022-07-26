import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ComplexityValidator:
    """
     @Time    : 2022年4月25日
     @Author  : xiaosong
     @Description    : 验证密码复杂度
    """
    message = _("必须更加复杂 (%s)")
    code = "complexity"

    def __init__(self, password, complexities):
        # print(password)
        # print('初始化')
        self.password = password
        self.complexity = complexities

    def __call__(self, *args, **kwargs):
        # print("验证")
        if self.complexity is None:
            return
        uppercase, lowercase, letters = set(), set(), set()
        digits, special = set(), set()

        for character in self.password:
            if character.isupper():
                uppercase.add(character)
                letters.add(character)
            elif character.islower():
                lowercase.add(character)
                letters.add(character)
            elif character.isdigit():
                digits.add(character)
            elif not character.isspace():
                special.add(character)

        words = set(re.findall(r'\b\w+', self.password, re.UNICODE))
        errors = []
        if len(uppercase) < self.complexity.get("UPPER", 0):
            errors.append(
                _("%(UPPER)s 个及以上不同的大写字母") %
                self.complexity)
        if len(lowercase) < self.complexity.get("LOWER", 0):
            errors.append(
                _("%(LOWER)s 个及以上不同的小写字母") %
                self.complexity)
        if len(letters) < self.complexity.get("LETTERS", 0):
            errors.append(
                _("%(LETTERS)s 个及以上不同的大小写字母") %
                self.complexity)
        if len(digits) < self.complexity.get("DIGITS", 0):
            errors.append(
                _("%(DIGITS)s 个及以上不同的数字") %
                self.complexity)
        if len(special) < self.complexity.get("SPECIAL", 0):
            errors.append(
                _("%(SPECIAL)s 个及以上的特殊字符") %
                self.complexity)
        if len(words) < self.complexity.get("WORDS", 0):
            errors.append(
                _("%(WORDS)s 个及以上不同的单词") %
                self.complexity)
        # print(errors)
        if errors:
            raise ValidationError(self.message % (_(u'必须包含 ') + u', '.join(errors),), code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.complexity == other.complexity
            and self.password == other.password
                )
