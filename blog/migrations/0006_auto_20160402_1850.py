# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160402_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.FilePathField(),
        ),
    ]