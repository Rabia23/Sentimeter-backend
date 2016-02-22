# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_remove_question_ispromotion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='genreType',
        ),
    ]
