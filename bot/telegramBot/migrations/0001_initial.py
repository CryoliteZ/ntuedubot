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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=50)),
                ('information', models.TextField(verbose_name='information')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('cid', models.CharField(verbose_name='ID', serialize=False, max_length=9, primary_key=True)),
                ('semester', models.IntegerField(verbose_name='semester')),
                ('name', models.CharField(verbose_name='Name', max_length=50)),
                ('courseNum', models.CharField(verbose_name='courseNum', max_length=50)),
                ('classNo', models.CharField(verbose_name='classNo', max_length=50, blank=True)),
                ('credit', models.IntegerField(verbose_name='Credit', blank=True)),
                ('time', models.CharField(verbose_name='calssTime', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=50)),
                ('action', models.TextField(verbose_name='action')),
            ],
        ),
        migrations.CreateModel(
            name='Event_Occur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('cid', models.ForeignKey(to='telegramBot.Course', max_length=9)),
                ('eid', models.ForeignKey(to='telegramBot.Event', max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='GRADE',
            fields=[
                ('courseID', models.CharField(verbose_name='courseID', serialize=False, max_length=20, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('isbotmessage', models.BooleanField(verbose_name='isbotmessage')),
                ('context', models.TextField(verbose_name='context')),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='food', max_length=50)),
                ('phone', models.CharField(verbose_name='food', max_length=50)),
                ('startTime', models.TimeField(verbose_name='startTime')),
                ('EndTime', models.TimeField(verbose_name='EndTime')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('name', models.CharField(verbose_name='name', serialize=False, max_length=9, primary_key=True)),
                ('location', models.CharField(verbose_name='location', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Store_food',
            fields=[
                ('food', models.CharField(verbose_name='food', max_length=50)),
                ('price', models.IntegerField(verbose_name='price', serialize=False, primary_key=True)),
                ('sid', models.ForeignKey(to='telegramBot.Store')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sid', models.CharField(verbose_name='ID', serialize=False, max_length=9, primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=50)),
                ('department', models.CharField(verbose_name='department', max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='takeCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('cid', models.ForeignKey(to='telegramBot.Course', max_length=9)),
                ('sid', models.ForeignKey(to='telegramBot.Student', max_length=9)),
            ],
        ),
    ]
