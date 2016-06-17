# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0008_remove_userinfo_objectid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
