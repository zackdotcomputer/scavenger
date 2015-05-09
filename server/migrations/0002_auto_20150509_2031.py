# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='shortname',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=models.CharField(max_length=40, null=True, verbose_name=b'Phone number'),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
