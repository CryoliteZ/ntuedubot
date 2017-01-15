# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegramBot', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='takeCourse',
            new_name='Take_Course',
        ),
        migrations.AlterField(
            model_name='course',
            name='time',
            field=models.CharField(verbose_name='classTime', max_length=15),
        ),
    ]
