# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_auto_20160308_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='action_comment',
            field=models.CharField(blank=True, db_index=True, null=True, max_length=1000),
        ),
    ]
