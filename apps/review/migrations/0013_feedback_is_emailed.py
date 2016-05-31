# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0012_concern_color_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_emailed',
            field=models.BooleanField(default=True),
        ),
    ]
