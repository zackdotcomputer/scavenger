# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hint', models.CharField(max_length=200, verbose_name=b'Clue hint text')),
                ('bonus', models.CharField(max_length=200, verbose_name=b'Optional bonus text')),
                ('solutions', models.CharField(max_length=200, verbose_name=b'Comma separated Foursquare venue ID solutions')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'name')),
                ('start_time', models.DateTimeField(verbose_name=b'game start')),
                ('end_time', models.DateTimeField(verbose_name=b'game end')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=40, verbose_name=b'Phone number')),
                ('foursqId', models.BigIntegerField(verbose_name=b'Foursquare User ID')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(verbose_name=b'solution time')),
                ('clue', models.ForeignKey(to='server.Clue')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'team name')),
                ('course', models.ManyToManyField(to='server.Clue')),
                ('players', models.ManyToManyField(to='server.Player')),
            ],
        ),
        migrations.AddField(
            model_name='progress',
            name='team',
            field=models.ForeignKey(to='server.Team'),
        ),
        migrations.AddField(
            model_name='clue',
            name='game',
            field=models.ForeignKey(to='server.Game'),
        ),
    ]
