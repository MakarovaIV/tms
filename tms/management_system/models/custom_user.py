from django.contrib.auth.models import AbstractUser
from django.db import models

from ..managers import CustomUserManager


class CustomUser(AbstractUser):
    class Types(models.TextChoices):
        OWNER = "Owner", "Owner"
        EMPLOYEE = "Developer", "Developer"
        TESTER = "Tester", "Tester"

    type = models.CharField(choices=Types.choices, default=Types.TESTER)
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

