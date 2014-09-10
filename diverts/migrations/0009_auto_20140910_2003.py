# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0008_airfield_icao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airfield',
            name='icao',
            field=models.CharField(max_length=5),
        ),
    ]
