# Generated by Django 2.2.16 on 2022-01-19 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220119_1252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['-name'], 'verbose_name': 'жанр', 'verbose_name_plural': 'жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-name'], 'verbose_name': 'произведение', 'verbose_name_plural': 'произведения'},
        ),
    ]