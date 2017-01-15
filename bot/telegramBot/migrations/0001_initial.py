# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('information', models.TextField(verbose_name='information')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('cid', models.CharField(serialize=False, max_length=9, primary_key=True, verbose_name='ID')),
                ('semester', models.IntegerField(verbose_name='semester')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('courseNum', models.CharField(max_length=50, verbose_name='courseNum')),
                ('classNo', models.CharField(max_length=50, verbose_name='classNo', blank=True)),
                ('credit', models.IntegerField(verbose_name='Credit', blank=True)),
                ('time', models.CharField(max_length=15, verbose_name='classTime')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('action', models.TextField(verbose_name='action')),
            ],
        ),
        migrations.CreateModel(
            name='Event_Occur',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('cid', models.ForeignKey(max_length=9, to='telegramBot.Course')),
                ('eid', models.ForeignKey(max_length=9, to='telegramBot.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('courseID', models.CharField(serialize=False, max_length=20, primary_key=True, verbose_name='courseID')),
                ('semester', models.IntegerField(verbose_name='semester')),
                ('gradeA1', models.IntegerField(verbose_name='AplusNum')),
                ('gradeA2', models.IntegerField(verbose_name='ANum')),
                ('gradeA3', models.IntegerField(verbose_name='AminusNum')),
                ('gradeB1', models.IntegerField(verbose_name='BplusNum')),
                ('gradeB2', models.IntegerField(verbose_name='BNum')),
                ('gradeB3', models.IntegerField(verbose_name='BminusNum')),
                ('gradeC1', models.IntegerField(verbose_name='CplusNum')),
                ('gradeC2', models.IntegerField(verbose_name='CNum')),
                ('gradeC3', models.IntegerField(verbose_name='CminusNum')),
                ('gradeF', models.IntegerField(verbose_name='FNum')),
                ('predictable', models.BooleanField(verbose_name='Predictable')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('isbotmessage', models.BooleanField(verbose_name='isbotmessage')),
                ('context', models.TextField(verbose_name='context')),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50, verbose_name='food')),
                ('phone', models.CharField(max_length=50, verbose_name='food')),
                ('startTime', models.TimeField(verbose_name='startTime')),
                ('EndTime', models.TimeField(verbose_name='EndTime')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('name', models.CharField(serialize=False, max_length=9, primary_key=True, verbose_name='name')),
                ('location', models.CharField(max_length=50, verbose_name='location')),
                ('phone', models.CharField(max_length=15, verbose_name='phonenum')),
            ],
        ),
        migrations.CreateModel(
            name='Store_Food',
            fields=[
                ('food', models.CharField(max_length=50, verbose_name='food')),
                ('price', models.IntegerField(serialize=False, primary_key=True, verbose_name='price')),
                ('sid', models.ForeignKey(to='telegramBot.Store')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sid', models.CharField(serialize=False, max_length=9, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('department', models.CharField(max_length=20, verbose_name='department', blank=True)),
                ('chat_id', models.CharField(max_length=50, verbose_name='chat_id')),
            ],
        ),
        migrations.CreateModel(
            name='Take_Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('cid', models.ForeignKey(max_length=9, to='telegramBot.Course')),
                ('sid', models.ForeignKey(max_length=9, to='telegramBot.Student')),
            ],
        ),
    ]
