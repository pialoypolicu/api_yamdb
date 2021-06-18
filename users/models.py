from django.contrib.auth.hashers import \
    check_password as check_confirmation_code
from django.contrib.auth.hashers import make_password as make_confirmation_code
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.utils import wrap_text


class AnonymousUser(DjangoAnonymousUser):  # noqa
    role = None


class UserManager(DefaultUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        return super().create_superuser(username, email=None, password=None, **extra_fields)


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(
        null=True,
        blank=True,
        default='',
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

    objects = UserManager()

    _confirmation_code = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def set_confirmation_code(self, raw_confirmation_code):
        self.confirmation_code = make_confirmation_code(raw_confirmation_code)
        self._confirmation_code = raw_confirmation_code

    def check_confirmation_code(self, raw_confirmation_code):
        def setter(raw_confirmation_code):
            self.set_password(raw_confirmation_code)
            self._confirmation_code = None
            self.save(update_fields=['password'])

        return check_confirmation_code(
            raw_confirmation_code,
            self.confirmation_code,
            setter
        )

    def __str__(self):
        bio = wrap_text(self.bio)
        return (
            f'id: {self.id}\n'
            f'username: {self.username}\n'
            f'email: {self.email}\n'
            f'role: {self.role}\n'
            f'bio: {bio}\n'
        )
