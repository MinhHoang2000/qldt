from drf_yasg import openapi

PERSON_REQUIRED = ['first_name', 'last_name', 'gender', 'date_of_birth', 'address']

PERSON_PROP = {
    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
    'gender': openapi.Schema(type=openapi.TYPE_STRING, description='M or F'),
    'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, description='Date of birth'),
    'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
    'ethnicity': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
    'religion': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
    'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
}

HEALTH_PROP = {
   'height': openapi.Schema(type=openapi.TYPE_INTEGER, description='Height'),
    'weight': openapi.Schema(type=openapi.TYPE_INTEGER, description='Weight'),
    'eye_sight': openapi.Schema(type=openapi.TYPE_INTEGER, description='from 0 to 10'),
    'health_status': openapi.Schema(type=openapi.TYPE_STRING, description='Health status'),
    'disease': openapi.Schema(type=openapi.TYPE_STRING, description='Disease'),
}
