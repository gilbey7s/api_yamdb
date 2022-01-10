# Generated by Django 2.2.16 on 2022-01-08 13:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220107_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(help_text='Введите год в формате: YYYY', validators=[django.core.validators.MinValueValidator(1100), django.core.validators.MaxValueValidator(2022)], verbose_name='год'),
        ),
    ]
