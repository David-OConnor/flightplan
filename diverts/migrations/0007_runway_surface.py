# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0006_auto_20140909_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='runway',
            name='surface',
            field=models.CharField(default='EMPTY', max_length=30),
            preserve_default=False,
        ),
    ]
