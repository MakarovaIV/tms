from django.db import models

from .custom_user import CustomUser
from .project import Project
from .suit import Suit
from .test_case_in_test_plan import TCinTP

TP_STATUS = [
    ("IN PROGRESS", "IN PROGRESS"),
    ("DONE", "DONE"),
    ("CANCELLED", "CANCELLED"),
]

TC_IN_TP_STATUS = [
    ("IN PROGRESS", "IN PROGRESS"),
    ("SUCCEED", "SUCCEED"),
    ("FAILED", "FAILED"),
    ("SKIPPED", "SKIPPED"),
]


class TP(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    modified_by = models.IntegerField()
    proj = models.ManyToManyField(Project)
    suit = models.ManyToManyField(Suit)
    tc = models.ManyToManyField(TCinTP)
    status = models.CharField(choices=TP_STATUS, default="IN PROGRESS", null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ' \
               f'{self.desc} ' \
               f'{self.user} ' \
               f'{self.modified_by} ' \
               f'{self.tc} ' \
               f'{self.proj} ' \
               f'{self.suit} ' \
               f'{self.status} ' \
               f'{self.creation_date} ' \
               f'{self.modification_date}'