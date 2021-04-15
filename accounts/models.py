from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.utils import timezone
from django.contrib.auth.models import _user_has_perm


#persmission table
class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=128)
    permission_code = models.CharField(max_length=4)

    class Meta:
        db_table = 'permission'


class Account(AbstractBaseUser):
    username = models.CharField('username',
                                max_length=128,
                                unique=True,
                                help_text='Username is required. Fewer than 256 character',
                                validators=[UnicodeUsernameValidator()],
                                error_messages={'unique': 'Username already exists'})

    email = models.CharField('email address', max_length=320, validators=[EmailValidator()])
    is_admin = models.BooleanField('admin permisson', default=False)
    is_active = models.BooleanField('active', default=True)
    join_at = models.DateTimeField('join at', default=timezone.now)

    # Create new table account_permission
    permissions = models.ManyToManyField(Permission, related_name='account', db_table='account_permissions')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_staff:
            return True
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'account'
