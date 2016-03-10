# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0002_option_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='color_code',
            field=models.CharField(max_length=20, blank=True, null=True),
            preserve_default=False,
        ),
    ]
