# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0013_feedback_is_emailed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='objectId',
        ),
    ]
