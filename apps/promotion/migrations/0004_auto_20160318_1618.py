# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_boto.s3.storage


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0003_auto_20160315_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='background_image',
            field=models.ImageField(null=True, storage=django_boto.s3.storage.S3Storage(), upload_to='promotions', blank=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='banner_image',
            field=models.ImageField(null=True, storage=django_boto.s3.storage.S3Storage(), upload_to='promotions', blank=True),
        ),
    ]
