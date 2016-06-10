# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0011_feedback_segment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='objectId',
        ),
    ]
