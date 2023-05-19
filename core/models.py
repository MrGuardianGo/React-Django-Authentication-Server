from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=50)
    status = models.TextField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=5000)
    avatar = models.CharField(max_length=10000, blank=True, null=True, default='default.jpg')
    friends = models.ManyToManyField('self', blank=True, null=True)
    username = None
    first_name = None
    last_name = None
    last_login = None
    is_superuser = None
    is_staff = None
    is_active = None
    date_joined = None
    groups = None
    user_permissions = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()