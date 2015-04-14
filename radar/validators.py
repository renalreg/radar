from collections import defaultdict


class Validator(object):
    validators = {}

    def __init__(self, obj):
        self.obj = obj
        self._reset()

    def _reset(self):
        self.errors = defaultdict(list)

    def _valid(self):
        return not any(len(x) for x in self.errors)

    def _validate(self):
        self._reset()

        for model_attr, validators in self.validators.items():
            model_value = getattr(self.obj, model_attr)

            for validator in validators:
                try:
                    validator(model_value)
                except ValidationError as e:
                    self.errors[model_attr].append(e)
                    break
                except StopValidation:
                    break

        if not self._valid():
            return

        self.validate()

    def validate(self):
        pass

    def valid(self):
        self._validate()
        return self._valid()

class FormValidator(Validator):
    def validate_concepts(self):
        concepts = self.obj.to_concepts()

        for concept, field_mappings in concepts:
            if not concept.valid():
                for model_field, concept_field in field_mappings:
                    self.errors[model_field].extend(concept.errors[concept_field])

    def validate(self):
        self.validate_concepts()

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

class StopValidation(Exception):
    pass

def required(value):
    if value is None:
        raise ValidationError('This field is required.')

def not_empty(value):
    if value is None or len(value) == 0:
        raise ValidationError('This field is required.')

def optional(value):
    if value is None:
        raise StopValidation()