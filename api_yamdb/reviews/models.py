import datetime
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .validators import validate_me


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='название',
                            unique=True
                            )
    slug = models.SlugField(unique=True, verbose_name='уникальный id')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='название',
                            unique=True
                            )
    slug = models.SlugField(unique=True, verbose_name='уникальный id')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='название')
    year = models.PositiveSmallIntegerField(
        verbose_name='год',
        validators=[
            MinValueValidator(1100),
            MaxValueValidator(datetime.datetime.now().year)],
        help_text='Введите год в формате: YYYY'
    )
    description = models.TextField(verbose_name='описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='категория'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name, self.year, self.category


class GenreTitle(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='genres',
                              verbose_name='произведение'
                              )
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              related_name='titles',
                              verbose_name='жанр'
                              )

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'
        constraints = [
            UniqueConstraint(fields=['title', 'genre'],
                             name='unique_genre_title')
        ]


USER = _("user")
MODERATOR = _("moderator")
ADMIN = _("admin")

DICT_ROLE = [
    (USER, _("user")),
    (MODERATOR, _("moderator")),
    (ADMIN, _("admin")),
]


class CustomUser(AbstractUser):

    email = models.EmailField(_("email address"), unique=True, max_length=254,)
    bio = models.TextField(_("biography"), blank=True,)
    role = models.CharField(_("user role"), max_length=16, choices=DICT_ROLE, default=USER, blank=True,)
    confirmation_code = models.IntegerField(_("code"), default=0,)
    username = models.CharField(_("username"), validators=(validate_me,), unique=True, max_length=150,)

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ['-username', ]
