# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0011_feedback_segment'),
    ]

    operations = [
        migrations.AddField(
            model_name='concern',
            name='color_code',
            field=models.CharField(null=True, max_length=20, blank=True),
        ),
    ]
