from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Ingredient
from .models import Recipe

import json

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def index(request):
	ingredient_list = Ingredient.objects.all()
	template = loader.get_template('finderApp/index.html')
	context = {
		'ingredient_list': ingredient_list,
	}
	return HttpResponse(template.render(context, request))

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/finderApp/")
	else:
		form = UserCreationForm()
	return render(request, 'finderApp/signup.html', {'form': form})

def search_result(request):
	template = loader.get_template('finderApp/search_result.html')

	ingredient_list = []
	if request.method == "GET":
		ingredient_list_string = request.GET['ingredient_list']
		# json decode
		ingredient_list = json.loads(ingredient_list_string)

	result_list = ingredient_list
	context = {
		'recipe_list': result_list,
		'dummy_recipe_id': 1,
	}
	return HttpResponse(template.render(context, request))

def recipe(request, recipe_id):
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	return render(request, 'finderApp/recipe_detail.html', {'recipe': recipe})