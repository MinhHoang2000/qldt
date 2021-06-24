from drf_yasg import openapi

SIGNUP_ACCOUNT_PROP = {
    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
    'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
    'is_admin': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is admin')
}

PERMISSION_PROP = {
    'permission_name': openapi.Schema(type=openapi.TYPE_STRING, description='Description permission'),
    'permission_code': openapi.Schema(type=openapi.TYPE_STRING, description='For checking permission'),
}
