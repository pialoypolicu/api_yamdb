from django.contrib.auth.hashers import make_password as make_confirmation_code
from django.contrib.auth.hashers import check_password as check_confirmation_code
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.utils import get_username_from_email, wrap_text


class AnonymousUser(DjangoAnonymousUser):  # noqa
    role = None


class UserManager(DjangoUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        username = username or get_username_from_email(email)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        username = username or get_username_from_email(email)

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(_('email address'), unique=True)
    description = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=100,
        choices=Roles.choices,
        default=Roles.USER,
    )
    confirmation_code = models.CharField(
        _('confirmation_code'),
        max_length=128,
    )

    _confirmation_code = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    # objects = UserManager()

    def set_confirmation_code(self, raw_confirmation_code):
        self.confirmation_code = make_confirmation_code(raw_confirmation_code)
        self._confirmation_code = raw_confirmation_code

    def check_confirmation_code(self, raw_confirmation_code):
        def setter(raw_confirmation_code):
            self.set_password(raw_confirmation_code)
            self._confirmation_code = None
            self.save(update_fields=["password"])

        return check_confirmation_code(raw_confirmation_code, self.confirmation_code, setter)

    def __str__(self):
        bio = wrap_text(self.description)
        return (
            f'id: {self.id}\n'
            f'username: {self.username}'
            f'email: {self.email}'
            f'role: {self.role}'
            f'bio: {bio}'
        )
