# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_remove_concern_color_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='segment',
            field=models.IntegerField(null=True, db_index=True, blank=True),
        ),
    ]
