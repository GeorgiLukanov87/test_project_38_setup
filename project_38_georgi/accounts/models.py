from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models


class TestUser(auth_models.AbstractUser):
    username = models.CharField(
        max_length=30,
        validators=[
            validators.MinLengthValidator(3, message='Username must be at least 3 characters long')
        ]
    )

    email = models.EmailField(
        max_length=200,
        unique=True
    )
