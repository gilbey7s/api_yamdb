from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .validators import validate_me


USER = _("user")
MODERATOR = _("moderator")
ADMIN = _("admin")

DICT_ROLE = (
    (USER, _("user")),
    (MODERATOR, _("moderator")),
    (ADMIN, _("admin")),
)


class CustomUser(AbstractUser):

    email = models.EmailField(_("email address"), unique=True, max_length=254,)
    bio = models.TextField(_("biography"), blank=True,)
    role = models.CharField(_("user role"), max_length=16, choices=DICT_ROLE, default=USER, blank=True,)
    confirmation_code = models.IntegerField(_("code"), default=0,)
    username = models.CharField(_("username"), validators=(validate_me,), unique=True, max_length=150,)
