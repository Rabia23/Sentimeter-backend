# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0008_remove_feedback_gro_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='concern',
            name='color_code',
            field=models.CharField(null=True, blank=True, max_length=20),
        ),
    ]
