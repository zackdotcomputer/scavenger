# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20150509_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='game',
            field=models.ForeignKey(default='0', to='server.Game'),
            preserve_default=False,
        ),
    ]
