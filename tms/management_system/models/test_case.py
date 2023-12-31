from django.db import models

from .custom_user import CustomUser
from .project import Project
from .suit import Suit


TC_STATUS = [
    ("ACTIVE", "ACTIVE"),
    ("DRAFT", "DRAFT"),
    ("OUTDATED", "OUTDATED"),
]
TC_PRIORITY = [
    ("HIGH", "HIGH"),
    ("MEDIUM", "MEDIUM"),
    ("LOW", "LOW"),
]


class TC(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    modified_by = models.IntegerField()
    proj = models.ForeignKey(Project, on_delete=models.CASCADE)
    suit = models.ForeignKey(Suit, on_delete=models.CASCADE)
    status = models.CharField(choices=TC_STATUS, default="DRAFT")
    steps = models.JSONField(blank=True)
    priority = models.CharField(choices=TC_PRIORITY, default="MEDIUM")
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ' \
               f'{self.desc} ' \
               f'{self.user} ' \
               f'{self.modified_by} ' \
               f'{self.proj} ' \
               f'{self.suit} ' \
               f'{self.status} ' \
               f'{self.steps} ' \
               f'{self.creation_date} ' \
               f'{self.modification_date}'
