# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-01 01:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finderApp', '0003_ingredient_picture_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_direction', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='picture_url',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='contained_ingredient',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='recipe_name',
        ),
        migrations.AddField(
            model_name='recipe',
            name='catogery',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='recipe',
            name='contained_ingredients',
            field=models.ManyToManyField(to='finderApp.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='recipe',
            name='name',
            field=models.CharField(default='no name', max_length=200),
        ),
        migrations.AddField(
            model_name='recipe',
            name='servings',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='recipe',
            name='directions',
            field=models.ManyToManyField(to='finderApp.Direction'),
        ),
    ]
