# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0007_auto_20160317_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='objectId',
        ),
    ]
