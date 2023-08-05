from typing import Type

from django.db.models import IntegerChoices
from rest_framework.serializers import ChoiceField as BaseChoiceField

__version__ = '0.0.3'
__author__ = 'Haoyu Pan'
__email__ = 'panhaoyu.china@outlook.com'


class RestDisplayChoiceField(BaseChoiceField):
    def __init__(self, choices, **kwargs):
        self._dict_int_to_choice = {k: v for k, v in choices}
        self._dict_choice_to_int = {v: k for k, v in choices}
        choices = [v for k, v in choices]
        super().__init__(choices, **kwargs)

    def to_representation(self, value):
        try:
            return self._dict_int_to_choice[value]
        except KeyError:
            self.fail('invalid_choice', input=value)

    def to_internal_value(self, data):
        try:
            return self._dict_choice_to_int[data]
        except KeyError:
            self.fail('invalid_choice', input=data)


class RestDisplayIntegerChoiceField(RestDisplayChoiceField):
    def __init__(self, choices: Type[IntegerChoices], **kwargs):
        """Choice field that display the str and save int in database."""
        self.__choices = choices
        parsed_choices = [(choice.value, choice.name) for choice in choices]
        super().__init__(parsed_choices, **kwargs)

    def to_internal_value(self, data):
        try:
            return self.__choices[data]
        except:
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        # noinspection PyCallingNonCallable
        return self.__choices(value).name

    @property
    def names(self):
        return [choice.name for choice in self.__choices]

    @property
    def option_metadata(self):
        return [{'name': choice.name} for choice in self.__choices]
