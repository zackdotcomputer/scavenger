# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20150509_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clue',
            name='game',
        ),
        migrations.RemoveField(
            model_name='game',
            name='cluesPer',
        ),
        migrations.RemoveField(
            model_name='game',
            name='completionMessage',
        ),
        migrations.RemoveField(
            model_name='game',
            name='instructions',
        ),
        migrations.RemoveField(
            model_name='team',
            name='game',
        ),
        migrations.RemoveField(
            model_name='team',
            name='players',
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(default=0, to='server.Team'),
            preserve_default=False,
        ),
    ]
