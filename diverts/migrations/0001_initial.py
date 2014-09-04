# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airfield',
            fields=[
                ('ident', models.CharField(primary_key=True, max_length=6, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('control', models.CharField(max_length=100)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Airway',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('navaids', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jetway',
            fields=[
                ('airway_ptr', models.OneToOneField(to='diverts.Airway', primary_key=True, parent_link=True, serialize=False, auto_created=True)),
            ],
            options={
            },
            bases=('diverts.airway',),
        ),
        migrations.CreateModel(
            name='Navaid',
            fields=[
                ('ident', models.CharField(primary_key=True, max_length=6, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('components', models.CharField(max_length=500)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notam',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Runway',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('number', models.CharField(max_length=50)),
                ('length', models.IntegerField()),
                ('width', models.IntegerField()),
                ('airfield', models.ForeignKey(to='diverts.Airfield')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
