from drf_yasg import openapi

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
