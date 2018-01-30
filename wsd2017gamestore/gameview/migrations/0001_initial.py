# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-30 12:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HighScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
