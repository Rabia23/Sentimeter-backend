# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0006_userinfo_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='ageGroup',
            field=models.IntegerField(null=True, blank=True, db_index=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='gender',
            field=models.IntegerField(null=True, blank=True, db_index=True),
        ),
    ]
