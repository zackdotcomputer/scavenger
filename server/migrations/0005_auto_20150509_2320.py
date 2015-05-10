# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_team_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='completionMessage',
            field=models.CharField(default=b'', max_length=140, verbose_name=b'completion message'),
        ),
        migrations.AddField(
            model_name='game',
            name='instructions',
            field=models.CharField(default=b'', max_length=500, verbose_name=b'instructions'),
        ),
    ]
