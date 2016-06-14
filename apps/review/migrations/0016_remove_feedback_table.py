# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0015_remove_feedback_objectid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='table',
        ),
    ]
