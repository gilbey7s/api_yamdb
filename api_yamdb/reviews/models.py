import datetime

from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator


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
