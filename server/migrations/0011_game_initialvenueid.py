# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0010_team_courseorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='initialVenueId',
            field=models.CharField(default=b'', max_length=30, verbose_name=b'inital venue id'),
        ),
    ]
