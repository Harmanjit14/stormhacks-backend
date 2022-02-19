# Generated by Django 3.1.7 on 2022-02-19 07:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]