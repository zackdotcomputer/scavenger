# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20150509_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='cluesPer',
            field=models.IntegerField(default=4, verbose_name=b'clues per team'),
        ),
    ]
