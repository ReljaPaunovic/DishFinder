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

def search_result(request, search_param):
	return HttpResponse("You're at recipe search result page.")

def recipe(request, recipe_id):
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	return render(request, 'finderApp/recipe_detail.html', {'recipe': recipe})