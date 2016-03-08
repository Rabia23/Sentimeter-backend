# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_concern_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 8, 12, 50, 57, 140164, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='updated_at',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
    ]
