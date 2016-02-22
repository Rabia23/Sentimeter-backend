# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_remove_question_genretype'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='genreType',
            field=models.IntegerField(db_index=True, blank=True, null=True),
        ),
    ]
