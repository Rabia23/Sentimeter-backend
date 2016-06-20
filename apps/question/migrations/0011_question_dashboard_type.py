# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0010_auto_20160609_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='dashboard_type',
            field=models.IntegerField(default=0, db_index=True),
        ),
    ]
