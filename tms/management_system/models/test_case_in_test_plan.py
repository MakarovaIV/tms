from django.db import models

from .custom_user import CustomUser
from .test_plan import TP
from .test_case import TC


TC_IN_TP_STATUS = [
    ("IN PROGRESS", "IN PROGRESS"),
    ("SUCCEED", "SUCCEED"),
    ("FAILED", "FAILED"),
    ("SKIPPED", "SKIPPED"),
]


class TCinTP(models.Model):
    tc = models.ForeignKey(TC, on_delete=models.CASCADE)
    plan = models.ForeignKey(TP, on_delete=models.CASCADE, null=True)
    assignee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    tc_status = models.CharField(choices=TC_IN_TP_STATUS, default="IN PROGRESS")

    def __str__(self):
        return f'{self.tc} ' \
               f'{self.plan} ' \
               f'{self.assignee} ' \
               f'{self.tc_status}'
