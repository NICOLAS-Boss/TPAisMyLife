# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 14:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20160403_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo',
            field=models.ImageField(default=datetime.datetime(2016, 4, 3, 14, 37, 34, 336106, tzinfo=utc), upload_to=''),
            preserve_default=False,
        ),
    ]
