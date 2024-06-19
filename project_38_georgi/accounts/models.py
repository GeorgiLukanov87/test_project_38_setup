from django.db import models
from django.contrib.auth import models as auth_models


class TestUser(auth_models.AbstractUser):
    username = models.CharField(
        max_length=30
    )

    email = models.CharField(
        max_length=200,
        unique=True
    )
