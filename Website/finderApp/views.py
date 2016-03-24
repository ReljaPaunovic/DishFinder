from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

from .models import Ingredient
from .models import Recipe

def index(request):
	ingredient_list = Ingredient.objects.all()
	template = loader.get_template('finderApp/index.html')
	context = {
		'ingredient_list': ingredient_list,
	}
	return HttpResponse(template.render(context, request))

def search_result(request):
	template = loader.get_template('finderApp/search_result.html')

	ingredient_list = []
	if request.method == "GET":
		ingredient_list = request.GET['ingredient_list']
		print(ingredient_list)

	result_list = []
	context = {
		'recipe_list': ingredient_list,
	}
	return HttpResponse(template.render(context, request))

def recipe(request, recipe_id):
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	return render(request, 'finderApp/recipe_detail.html', {'recipe': recipe})