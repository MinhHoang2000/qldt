from drf_yasg import openapi
from accounts.schema import ACCOUNT_PROP, ACCOUNT_REQUIRED
from persons.schema import PERSON_PROP, PERSON_REQUIRED, HEALTH_PROP


STUDENT_PROP = {
    'account': openapi.Schema(type=openapi.TYPE_OBJECT, properties=ACCOUNT_PROP, required=ACCOUNT_REQUIRED, description='Account'),
    'person': openapi.Schema(type=openapi.TYPE_OBJECT,
                                     properties=PERSON_PROP,
                                     required=PERSON_REQUIRED,
                                     description='Personal Info'),
    'classroom_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Classroom id'),
    'status': openapi.Schema(type=openapi.TYPE_STRING, description='DH(Dang hoc) or DT(Dinh tri hoc) or TH(Thoi hoc)'),
    'admission_year': openapi.Schema(type=openapi.TYPE_INTEGER, description='Admission year'),
    'health':  openapi.Schema(type=openapi.TYPE_OBJECT, properties=HEALTH_PROP, description='Health condition'),
}

STUDENT_REQUIRED = ['account', 'classroom_id', 'person', 'status', 'admission_year']


GRADE_PROP = {
    'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Student id'),
    'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Course id'),
    'school_year':  openapi.Schema(type=openapi.TYPE_INTEGER, description='School year'),
    'semester':  openapi.Schema(type=openapi.TYPE_INTEGER, description='Semester'),
    'quiz1': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quiz 1'),
    'quiz2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quiz 2'),
    'quiz3': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quiz 3'),
    'test': openapi.Schema(type=openapi.TYPE_INTEGER, description='Test 15m'),
    'mid_term_test': openapi.Schema(type=openapi.TYPE_INTEGER, description='Test 45m'),
    'final_test': openapi.Schema(type=openapi.TYPE_INTEGER, description='Final test'),
    'start_update': openapi.Schema(type=openapi.TYPE_INTEGER, description='Time start updating grade'),
}

GRADE_REQUIRED = ['student_id', 'course_id', 'school_year', 'semester']

CONDUCT_PROP = {
    'score': openapi.Schema(type=openapi.TYPE_STRING, description='T or K or TB or Y'),
    'semester': openapi.Schema(type=openapi.TYPE_INTEGER, description='Semester'),
    'school_year': openapi.Schema(type=openapi.TYPE_INTEGER, description='School year'),
    'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Student id'),
}

CONDUCT_REQUIRED = ['score', 'semester', 'school_year', 'student_id']

PARENT_PROP = {
    'person': openapi.Schema(type=openapi.TYPE_OBJECT, properties=PERSON_PROP, description='Personal Info', required=PERSON_REQUIRED),
    'student_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description='List student id'),
    'avacation': openapi.Schema(type=openapi.TYPE_STRING, description='Avacation'),
}

PARENT_REQUIRED = ['person', 'avacation']
