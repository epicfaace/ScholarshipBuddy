from django.forms import fields
from django import forms
import jsonschema
from django.contrib.postgres.fields import JSONField
import json
from .schemas import JSONListFieldSchemas

class JSONSchemaField(JSONField):
    """
    A field that will ensure the data entered into it is valid JSON *and*
    internally validate to a JSON schema of your choice.
    Code initially from: https://stackoverflow.com/questions/33460690/django-models-add-validation-to-custom-field
    """
    def __init__(self, *args, **kwargs):
        super(JSONSchemaField, self).__init__(*args, **kwargs)

    def clean(self, raw_value, model_instance):
        """ Validates JSON on the proper schema
        (specified by self.name -- the field name serves as a key in the schemas dictionary)
        """
        try:
            jsonschema.validate(raw_value, JSONListFieldSchemas.schema[self.name])
        except (jsonschema.ValidationError, jsonschema.SchemaError) as err:
            raise forms.ValidationError(err.message)
        return super(JSONSchemaField, self).clean(raw_value, model_instance)

class JSONListSchemaField(JSONSchemaField):
    def __init__(self, *args, **kwargs):
        if 'schema' in kwargs: kwargs.pop('schema')
        #self.schema = kwargs.pop('schema', {})
        super(JSONListSchemaField, self).__init__(*args, **kwargs)

class ActivitiesField(JSONField):
    pass
class ScoresAPField(JSONField):
    pass