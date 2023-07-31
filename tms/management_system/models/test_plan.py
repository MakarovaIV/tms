from django.db import models

from .custom_user import CustomUser
from .project import Project
from .suit import Suit
from .test_case import TC


TC_STATUS = [
    ("ACTIVE", "ACTIVE"),
    ("DRAFT", "DRAFT"),
    ("OUTDATED", "OUTDATED"),
]

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
    desc = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    modified_by = models.IntegerField()
    proj = models.ForeignKey(Project, on_delete=models.RESTRICT)
    suit = models.ForeignKey(Suit, on_delete=models.RESTRICT)
    tc = models.ForeignKey(TC, on_delete=models.RESTRICT)
    status = models.CharField(choices=TP_STATUS, default="IN PROGRESS")
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    assignee = models.IntegerField()
    tc_status = models.CharField(choices=TC_IN_TP_STATUS, default="IN PROGRESS")

    def __str__(self):
        return f'{self.name} ' \
               f'{self.desc} ' \
               f'{self.user} ' \
               f'{self.modified_by} ' \
               f'{self.tc} ' \
               f'{self.proj} ' \
               f'{self.suit} ' \
               f'{self.status} ' \
               f'{self.assignee} ' \
               f'{self.tc_status} ' \
               f'{self.creation_date} ' \
               f'{self.modification_date}'
