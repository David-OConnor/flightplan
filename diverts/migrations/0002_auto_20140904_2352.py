# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airfield',
            name='control',
        ),
        migrations.AddField(
            model_name='airfield',
            name='aixm_id',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
