from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.DateField()
    description = models.TextField()
    genre = ''
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )


class GenreTitle(models.Model):
    pass
