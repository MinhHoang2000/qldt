from drf_yasg import openapi

SIGNUP_ACCOUNT_PROP = {
    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
    'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email')
}

SIGNUP_ACCOUNT_REQUIRED = ['username', 'password']

PERMISSION_PROP = {
    'permission_name': openapi.Schema(type=openapi.TYPE_STRING, description='Description permission'),
    'permission_code': openapi.Schema(type=openapi.TYPE_STRING, description='For checking permission'),
}
