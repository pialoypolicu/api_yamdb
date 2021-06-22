from django.db import models


class Roles(models.TextChoices):
    USER = 'user', 'User'
    MODERATOR = 'moderator', 'Moderator'
    ADMIN = 'admin', 'Admin'
