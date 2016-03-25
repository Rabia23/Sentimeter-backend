# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_question_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='text_urdu',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
