import uuid
from textwrap import fill, shorten

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def wrap_text(text: str) -> str:
    """Return beautifully wrapped text."""
    text = shorten(text, width=250, placeholder='...', initial_indent='\t')
    return fill(text, width=70)


def get_username_from_email(email: str) -> str:
    raw_username = email.split('@')[0]
    return ''.join(raw_username.split('.'))


def get_confirmation_code() -> str:
    return str(uuid.uuid4())


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'token': str(refresh.access_token),
    }


def send_confirmation_code(user, raw_confirmation_code):
    send_mail(
        'YaMDb confirmation code',
        f'Your confirmation code: {raw_confirmation_code}',
        'service@yamdb.com',
        [user.email],
        fail_silently=False,
    )
