# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0005_option_text_urdu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='objectId',
        ),
        migrations.AddField(
            model_name='option',
            name='sequence',
            field=models.IntegerField(null=True, blank=True, default=0),
        ),
    ]
