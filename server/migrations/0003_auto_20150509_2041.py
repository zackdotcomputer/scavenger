# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20150509_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=models.CharField(default=b'', max_length=40, verbose_name=b'Phone number', blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='shortname',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'Name', blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
