# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0003_option_color_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='objectId',
            field=models.CharField(db_index=True, null=True, blank=True, max_length=20),
        ),
    ]
