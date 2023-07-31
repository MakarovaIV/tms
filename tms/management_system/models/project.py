from django.db import models

from .custom_user import CustomUser


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
