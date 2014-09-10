# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0005_auto_20140908_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airfield',
            name='ident',
            field=models.CharField(primary_key=True, max_length=4, serialize=False),
        ),
        migrations.AlterField(
            model_name='navaid',
            name='ident',
            field=models.CharField(primary_key=True, max_length=3, serialize=False),
        ),
    ]
