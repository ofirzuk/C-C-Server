# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-10 13:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20160210_1432'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Data',
            new_name='DataItem',
        ),
    ]