# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-02 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finderApp', '0007_auto_20160402_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion', models.ManyToManyField(to='finderApp.Recipe')),
            ],
        ),
    ]