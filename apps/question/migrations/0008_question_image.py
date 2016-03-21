# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_boto.s3.storage


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_auto_20160315_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(upload_to='questions', null=True, blank=True, storage=django_boto.s3.storage.S3Storage()),
        ),
    ]
