# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0013_feedback_is_emailed'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='table',
            field=models.ForeignKey(blank=True, null=True, related_name='table', to='table.Table'),
        ),
    ]
