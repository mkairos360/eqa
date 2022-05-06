from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse

# Create your models here.

from evaluation_project import settings


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    is_student = models.BooleanField(default=False)
    is_qadmin = models.BooleanField(default=False)
    is_hadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE)
    choices = (
        ('100', 'Level 100'),
        ('200', 'Level 200'),
        ('300', 'Level 300'),
        ('400', 'Level 400'),
        ('600', 'Level 600'),
        ('700', 'Level 700'),
        ('800', 'Level 800'),
    )

    lecture_group = (
        ('day', 'Day'),
        ('evening', 'Evening'),
        ('weekend', 'Weekend'),
    )
    program = models.ForeignKey('core.Program', blank=False, null=True, on_delete=models.SET_NULL)
    course_group = models.CharField(max_length=30, choices=lecture_group,default="day", null=False, blank=False)
    level = models.CharField(max_length=30, choices=choices, null=False, blank=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name