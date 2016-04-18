# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0004_auto_20160315_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='text_urdu',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
