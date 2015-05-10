# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_game_cluesper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clue',
            name='bonus',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'Optional bonus text', blank=True),
        ),
    ]
