from drf_yasg import openapi

CLASSROOM_PROP = {
    'class_name' : openapi.Schema(type=openapi.TYPE_STRING, description='Classroom name'),
    'homeroom_teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Homeroom teacher id'),
    'location' : openapi.Schema(type=openapi.TYPE_STRING, description='Location'),
}

CLASSROOM_REQUIRED = ['class_name', 'homeroom_teacher_id', 'location']


COURSE_PROP = {
    'course_name': openapi.Schema(type=openapi.TYPE_STRING, description='Course name'),
    'group_course': openapi.Schema(type=openapi.TYPE_STRING, description='Sc for Science, So for society and Ph for physical'),
}

TIMETABLE_PROP = {
    'classroom_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Classroom id'),
    'teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Teacher id'),
    'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Course id'),
    'day_of_week': openapi.Schema(type=openapi.TYPE_STRING, description='Mon, Tue, Wed,..., Sun'),
    'shifts': openapi.Schema(type=openapi.TYPE_INTEGER, description='Shifts'),
    'semester': openapi.Schema(type=openapi.TYPE_INTEGER, description='Semester'),
    'school_year' : openapi.Schema(type=openapi.TYPE_INTEGER, description='Shool year'),
}

TIMETABLE_REQURIED = ['classroom_id', 'teacher_id', 'course_id', 'day_of_week', 'shifts', 'semester', 'school_year']

TIMETABLE_CHANGE_PROP = {
    'teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Teacher id'),
    'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Course id'),
}

CLASSRECORD_PROP = {
    'classroom_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Classroom id'),
    'teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Teacher id'),
    'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Course id'),
    'classification': openapi.Schema(type=openapi.TYPE_STRING, description='from A to F'),
    'study_week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Study week'),
    'day_of_week': openapi.Schema(type=openapi.TYPE_STRING, description='Mon, Tue, Wed,..., Sun'),
    'shifts': openapi.Schema(type=openapi.TYPE_INTEGER, description='Shifts'),
    'semester': openapi.Schema(type=openapi.TYPE_INTEGER, description='Semester'),
    'school_year' : openapi.Schema(type=openapi.TYPE_INTEGER, description='Shool year'),
    'attendant': openapi.Schema(type=openapi.TYPE_INTEGER, description='Attendant'),
    'note': openapi.Schema(type=openapi.TYPE_STRING, description='Note'),
}

CLASSRECORD_REQUIRED = ['classroom_id', 'teacher_id', 'course_id', 'day_of_week', 'shifts', 'study_week', 'attendant', 'semester', 'school_year', 'study_week']


CLASSRECORD_CHANGE_PROP = {
    'teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Teacher id, not necessary for teacher view'),
    'classification': openapi.Schema(type=openapi.TYPE_STRING, description='from A to F'),
    'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Course id'),
    'attendant': openapi.Schema(type=openapi.TYPE_INTEGER, description='Attendant'),
    'note': openapi.Schema(type=openapi.TYPE_STRING, description='Note'),
}

COURSE_REQUIRED = ['course_name', 'group_course']

DEVICE_PROP = {
    'status': openapi.Schema(type=openapi.TYPE_STRING, description='N for normal, B for broken, O for old'),
    'device_name': openapi.Schema(type=openapi.TYPE_STRING, description='Device name'),
    'price': openapi.Schema(type=openapi.TYPE_INTEGER, description='Price of each device'),
}


DEVICE_REQUIRED = ['status', 'device_name', 'price']

DEVICE_MANAGE_PROP = {
    'device_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Device id'),
    'day_of_week': openapi.Schema(type=openapi.TYPE_STRING, description='Mon, Tue, Wed,.., Sun'),
    'shifts': openapi.Schema(type=openapi.TYPE_INTEGER, description='Shifts'),
    'week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Week of study'),
    'teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Teacher id'),
}

TEACHER_DEVICE_MANAGE_PROP = {
    'device_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Device id'),
    'day_of_week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Mon, Tue, Wed,.., Sun'),
    'shifts': openapi.Schema(type=openapi.TYPE_INTEGER, description='Shifts'),
    'week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Week of study'),
}

DEVICE_MANAGE_REQUIRED = ['device_id', 'day_of_week', 'shifts', 'week', 'teacher_id']
TEACHER_DEVICE_MANAGE_REQUIRED = ['device_id', 'day_of_week', 'shifts', 'week']

STUDY_DOC_PROP = {
    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Title for the file'),
    'study_week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Week of study'),
    'teacher_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Teacher id'),
    'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Course id'),
    'classroom_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Classroom id'),
    'file': openapi.Parameter('file', openapi.IN_BODY, type=openapi.TYPE_FILE, description='File upload'),
}

TEACHER_STUDY_DOC_PROP = {
    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Title for the file'),
    'study_week': openapi.Schema(type=openapi.TYPE_INTEGER, description='Week of study'),
    'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Course id'),
    'classroom_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Classroom id'),
    'file': openapi.Parameter('file', openapi.IN_BODY, type=openapi.TYPE_FILE, description='File upload'),
}

STUDY_DOC_REQUIRED = ['name', 'study_week', 'teacher_id', 'course_id', 'classroom_id', 'file']
TEACHER_STUDY_DOC_REQUIRED = ['name', 'study_week', 'course_id', 'classroom_id', 'file']
