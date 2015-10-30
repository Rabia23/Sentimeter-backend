# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0011_auto_20151029_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 10, 15, 52, 984166, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedbackoption',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 10, 15, 57, 968287, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
