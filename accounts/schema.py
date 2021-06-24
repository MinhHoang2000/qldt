from drf_yasg import openapi

ACCOUNT_PROP = {
    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
    'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
}

CHANGE_PASS_PROP = {
    'current_password': openapi.Schema(type=openapi.TYPE_STRING, description='Old password'),
    'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
}
