# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_game_cluesper'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='courseOrder',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'course order'),
        ),
    ]
