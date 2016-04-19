# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0009_concern_color_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concern',
            name='color_code',
        ),
    ]
