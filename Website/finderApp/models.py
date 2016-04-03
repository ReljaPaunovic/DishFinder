from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Category model
class Category(models.Model):
	name = models.CharField(max_length=100, default="no name")

	def __str__(self):
		return self.name

# Recipe related models
class Ingredient(models.Model):
	ingredient_name = models.CharField(max_length=200)

	def __str__(self):
		return self.ingredient_name

class Direction(models.Model):
	recipe_direction = models.TextField()

	def __str__(self):
		return self.recipe_direction

class Recipe(models.Model):
	name = models.CharField(max_length=200, default="no name")
	image = models.URLField(max_length=200, default="")
	servings = models.PositiveSmallIntegerField(default=2)
	contained_ingredients = models.ManyToManyField(Ingredient)
	directions = models.ManyToManyField(Direction)
	category = models.ForeignKey(Category, null=True, blank=True, default=None)
	creater = models.ForeignKey(User, null=True, blank=True, default=None)

	def __str__(self):
		return self.name

# Meal model
class Meal(models.Model):
	suggestion = models.ManyToManyField(Recipe)