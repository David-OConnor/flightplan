# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diverts', '0002_auto_20140904_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fix',
            fields=[
                ('ident', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
