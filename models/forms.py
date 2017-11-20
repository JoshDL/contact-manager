from wtforms import Form, StringField, IntegerField, BooleanField, validators, ValidationError
import phonenumbers


# Registry Form Class
class RegistryForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=80), validators.required()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=80), validators.required()])
    phone = StringField('Phone')
    route = StringField('Street', [validators.Length(min=0, max=100)])
    locality = StringField('City', [validators.Length(min=0, max=100)])
    postal_code = IntegerField('Postal Code')
    country = StringField('Country', [validators.Length(min=0, max=100)])
    email = StringField('Email', [validators.Email(), validators.required()])
    web_page = StringField('Web', [validators.Optional()])

    @staticmethod
    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')


# Search Form Class
class SearchForm(Form):
    search_text = StringField('Search', [validators.Length(min=0, max=100)])
    search_field = StringField('Field')