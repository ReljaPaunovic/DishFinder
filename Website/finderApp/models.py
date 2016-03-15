from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Ingredient(models.Model):
	ingredient_name = models.CharField(max_length=200)
	picture_url = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.ingredient_name


class Recipe(models.Model):
	recipe_name = models.CharField(max_length=200)
	contained_ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

	def __str__(self):
		return self.recipe_name
