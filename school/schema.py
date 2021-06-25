from drf_yasg import openapi

COURSE_PROP = {
    'course_name': openapi.Schema(type=openapi.TYPE_STRING, description='Course name'),
    'group_course': openapi.Schema(type=openapi.TYPE_STRING, description='Sc for Science, So for society and Py for physical'),
}

COURSE_REQUIRED = ['course_name', 'group_course']

DEVICE_PROP = {
    'status': openapi.Schema(type=openapi.TYPE_STRING, description='N for normal, B for broken, O for old'),
    'device_name': openapi.Schema(type=openapi.TYPE_INTEGER, description='Device name'),
    'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='Amount of device'),
    'price': openapi.Schema(type=openapi.TYPE_INTEGER, description='Price of each device'),
}


DEVICE_REQUIRED = ['status', 'device_name', 'amount', 'price']

DEVICE_MANAGE_PROP = {
    'device_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Device id'),
    'day_of_week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Mon, Tue, Wed,.., Sun'),
    'shifts': openapi.Schema(type=openapi.TYPE_INTEGER, description='Shifts'),
    'week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Week of study'),
    'teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Teacher id'),
}

DEVICE_MANAGE_REQUIRED = ['device_id', 'day_of_week', 'shifts', 'week', 'teacher_id']

STUDY_DOC_PROP = {
    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Title for the file'),
    'study_week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Week of study'),
    'teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Teacher id'),
    'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Course id'),
    'classroom_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Classroom id'),
    'file': openapi.Parameter('file', openapi.IN_BODY, type=openapi.TYPE_FILE, description='File upload'),
}

STUDY_DOC_REQUIRED = ['name', 'study_week', 'teacher_id', 'course_id', 'classroom_id', 'file']
