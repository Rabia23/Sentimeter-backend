# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='objectId',
            field=models.CharField(db_index=True, null=True, max_length=20, blank=True),
        ),
    ]
