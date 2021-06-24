from drf_yasg import openapi
from accounts.schema import ACCOUNT_PROP, ACCOUNT_REQUIRED
from persons.schema import PERSON_PROP, PERSON_REQUIRED

TEACHER_PROP = {
    'account': openapi.Schema(type=openapi.TYPE_OBJECT, properties=ACCOUNT_PROP, required=ACCOUNT_REQUIRED, description='Account'),
    'person': openapi.Schema(type=openapi.TYPE_OBJECT, properties=PERSON_PROP, required=PERSON_REQUIRED, description='Personal Info'),

}

TEACHER_REQUIRED = ['account', 'person']
