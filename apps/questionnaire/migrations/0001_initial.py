# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0002_remove_branch_objectid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('isActive', models.BooleanField(default=True, db_index=True)),
                ('objectId', models.CharField(db_index=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('branch', models.ManyToManyField(related_name='questionnaire', to='branch.Branch')),
            ],
        ),
    ]
