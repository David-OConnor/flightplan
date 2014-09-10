# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0010_remove_airfield_icao'),
    ]

    operations = [
        migrations.AddField(
            model_name='airfield',
            name='icao',
            field=models.CharField(default='', max_length=5),
            preserve_default=False,
        ),
    ]
