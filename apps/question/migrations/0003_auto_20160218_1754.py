# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_question_genretype'),
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(null=True, related_name='questions', blank=True, to='questionnaire.Questionnaire'),
        ),
        migrations.AlterField(
            model_name='question',
            name='promotion',
            field=models.ForeignKey(null=True, related_name='questions', blank=True, to='promotion.Promotion'),
        ),
    ]
