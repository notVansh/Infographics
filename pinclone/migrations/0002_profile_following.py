# Generated by Django 3.2.3 on 2021-06-08 17:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pinclone', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, default='', null=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
    ]
