# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_game_initialvenueid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(to='server.Team', null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'solution time'),
        ),
    ]
