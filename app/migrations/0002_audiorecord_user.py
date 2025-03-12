# Generated by Django 5.1.7 on 2025-03-11 18:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
    migrations.AddField(
        model_name='audiorecord',
        name='user',
        field=models.ForeignKey(null=True, blank=True, to='auth.User', on_delete=models.CASCADE),
    ),
]
