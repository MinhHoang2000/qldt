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
