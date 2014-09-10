# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0009_auto_20140910_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airfield',
            name='icao',
        ),
    ]
