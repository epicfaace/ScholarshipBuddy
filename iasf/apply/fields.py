from django.forms import fields
from django import forms
import jsonschema
from django.contrib.postgres.fields import JSONField
import json
from .schemas import JSONListFieldSchemas
from validatedfile.fields import ValidatedFileField
from django.db import models

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

class DocumentField(ValidatedFileField):
#class DocumentField(models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs["content_types"] = ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/pdf", "image/png", "image/jpeg", "image/gif"]
        kwargs["max_upload_size"] = 10485760 # 10 MB
        # self.mime_lookup_length = kwargs.pop("mime_lookup_length", 4096)
        super(DocumentField, self).__init__(*args, **kwargs)


class ActivitiesField(JSONField):
    pass
class ScoresAPField(JSONField):
    pass