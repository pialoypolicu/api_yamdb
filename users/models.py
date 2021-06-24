from django.contrib.auth.hashers import check_password as check_code
from django.contrib.auth.hashers import make_password as make_confirmation_code
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.roles import Roles
from users.utils import wrap_text


class AnonymousUser(DjangoAnonymousUser):  # noqa
    role = None


class UserManager(DefaultUserManager):
    def create_superuser(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        return super().create_superuser(
            username,
            email,
            password,
            **extra_fields
        )


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(
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

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def set_confirmation_code(self, raw_confirmation_code):
        self.confirmation_code = make_confirmation_code(raw_confirmation_code)
        self._confirmation_code = raw_confirmation_code

    def check_confirmation_code(self, raw_confirmation_code):
        def setter(raw_confirmation_code):
            self.set_confirmation_code(raw_confirmation_code)
            self._confirmation_code = None
            self.save(update_fields=('confirmation_code',))

        return check_code(
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
