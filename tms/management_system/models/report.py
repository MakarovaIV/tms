from django.contrib.auth.models import AbstractUser
from django.db import models

from .test_plan import TP
from .custom_user import CustomUser


class Report(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(TP, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} '\
               f'{self.user} ' \
               f'{self.plan} ' \
               f'{self.creation_date}'
