# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0003_fix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fix',
            name='ident',
            field=models.CharField(serialize=False, primary_key=True, max_length=80),
        ),
    ]
