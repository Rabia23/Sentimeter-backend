# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_auto_20160315_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='objectId',
        ),
    ]
