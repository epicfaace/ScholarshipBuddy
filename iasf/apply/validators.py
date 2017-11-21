from django.core.validators import BaseValidator
from django.utils.translation import ungettext_lazy

class MaxWordsValidator(BaseValidator):
    message = ungettext_lazy(
        'Ensure this field has at most %(limit_value)d word (it has %(show_value)d).',
        'Ensure this field has at most %(limit_value)d words (it has %(show_value)d).',
        'limit_value')
    code = 'max_length'

    def compare(self, a, b):
        return a > b

    def clean(self, x):
        # Returns number of words.
        return len(x.split())