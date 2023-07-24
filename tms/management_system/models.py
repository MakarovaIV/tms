from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    picture = models.FileField(upload_to="tmp_upload")
    picture_data = models.BinaryField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} ' \
               f'{self.email} ' \
               f'{self.picture} ' \
               f'{self.creation_date}'


class Project(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} '\
               f'{self.desc} ' \
               f'{self.user} ' \
               f'{self.creation_date}'


# class TestCase(models.Model):
#     name = models.CharField(max_length=100)
#     desc = models.CharField(max_length=500, blank=True)
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
#     proj = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='user')
#     TC_STATUS = [
#         "ACTIVE",
#         "DRAFT",
#         "OUTDATED",
#     ]
#     status = models.CharField(choices=TC_STATUS, default="DRAFT")
#     steps = models.JSONField()
#     creation_date = models.DateTimeField(auto_now_add=True)
#     modification_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.name} ' \
#                f'{self.desc} ' \
#                f'{self.author} ' \
#                f'{self.proj} ' \
#                f'{self.status} ' \
#                f'{self.steps} ' \
#                f'{self.creation_date} ' \
#                f'{self.modification_date}'
#

