from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

TC_STATUS = [
    ("ACTIVE", "ACTIVE"),
    ("DRAFT", "DRAFT"),
    ("OUTDATED", "OUTDATED"),
]


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


class TC(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    modified_by = models.IntegerField()
    proj = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(choices=TC_STATUS, default="DRAFT")
    steps = models.JSONField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ' \
               f'{self.desc} ' \
               f'{self.user} ' \
               f'{self.modified_by} ' \
               f'{self.proj} ' \
               f'{self.status} ' \
               f'{self.steps} ' \
               f'{self.creation_date} ' \
               f'{self.modification_date}'


class TCHistory(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    modified_by = models.IntegerField()
    tc = models.ForeignKey(TC, on_delete=models.CASCADE)
    proj = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(choices=TC_STATUS, default="DRAFT")
    steps = models.JSONField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ' \
               f'{self.desc} ' \
               f'{self.user} ' \
               f'{self.modified_by} ' \
               f'{self.tc} ' \
               f'{self.proj} ' \
               f'{self.status} ' \
               f'{self.steps} ' \
               f'{self.creation_date} ' \
               f'{self.modification_date}'
