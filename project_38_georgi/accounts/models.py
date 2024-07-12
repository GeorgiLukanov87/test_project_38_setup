from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models


class TestUser(auth_models.AbstractUser):
    id = models.BigAutoField(
        primary_key=True,
    )

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

    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    last_modified_by = models.CharField(
        max_length=50
    )

    last_modified_date = models.DateTimeField(
        auto_now=True,
    )
