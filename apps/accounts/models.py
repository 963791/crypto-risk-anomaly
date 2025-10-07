from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # add profile fields as needed
    organization = models.CharField(max_length=128, blank=True, null=True)
    is_data_analyst = models.BooleanField(default=False)

    def __str__(self):
        return self.username
