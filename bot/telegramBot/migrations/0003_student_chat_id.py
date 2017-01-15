# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegramBot', '0002_auto_20170115_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='chat_id',
            field=models.CharField(default=0, max_length=50, verbose_name='chat_id'),
            preserve_default=False,
        ),
    ]
