# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_question_genretype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='objectId',
            field=models.CharField(null=True, max_length=20, db_index=True, blank=True),
        ),
    ]
