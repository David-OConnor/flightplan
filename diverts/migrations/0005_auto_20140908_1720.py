# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0004_auto_20140908_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airfield',
            name='ident',
            field=models.CharField(serialize=False, primary_key=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='fix',
            name='ident',
            field=models.CharField(serialize=False, primary_key=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='navaid',
            name='ident',
            field=models.CharField(serialize=False, primary_key=True, max_length=4),
        ),
    ]
