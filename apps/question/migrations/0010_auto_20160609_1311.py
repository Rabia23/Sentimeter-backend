# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0009_question_text_urdu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='objectId',
        ),
        migrations.AddField(
            model_name='question',
            name='sequence',
            field=models.IntegerField(null=True, blank=True, default=0),
        ),
    ]
