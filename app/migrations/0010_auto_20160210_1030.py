# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-10 08:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20160210_1002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='path',
            new_name='name',
        ),
    ]