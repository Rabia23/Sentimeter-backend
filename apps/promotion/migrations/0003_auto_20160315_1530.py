# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0002_auto_20160315_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='color_selected',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AddField(
            model_name='promotion',
            name='color_unselected',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AddField(
            model_name='promotion',
            name='toggle_colors',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
