from django.contrib.auth.models import AbstractUser
from django.db import models

from .custom_user import CustomUser
from .project import Project


class Suit(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    modified_by = models.IntegerField()
    proj = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} '\
               f'{self.desc} ' \
               f'{self.user} ' \
               f'{self.modified_by} ' \
               f'{self.proj} ' \
               f'{self.creation_date}'\
               f'{self.modification_date}'
