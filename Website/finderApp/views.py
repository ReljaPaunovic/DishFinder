from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

import json

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from .models import Ingredient
from .models import Recipe

from finderApp.login_service import login_service


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/finder/")
	else:
		form = UserCreationForm()
	return render(request, 'finderApp/signup.html', {'form': form})

def logout(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/finder/")

def index(request):
	login_err = login_service(request)['err_msg']
	ingredient_list = Ingredient.objects.all()
	template = loader.get_template('finderApp/index.html')
	context = {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'ingredient_list': ingredient_list,
	}
	return HttpResponse(template.render(context, request))

def search_result(request):
	login_err = login_service(request)['err_msg']
	template = loader.get_template('finderApp/search_result.html')

	ingredient_list = []
	if request.method == "GET":
		ingredient_list_string = request.GET['ingredient_list']
		# json decode
		ingredient_list = json.loads(ingredient_list_string)

	result_list = ingredient_list
	context = {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'recipe_list': result_list,
		'dummy_recipe_id': 1,
	}
	return HttpResponse(template.render(context, request))

def recipe(request, recipe_id):
	login_err = login_service(request)['err_msg']
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	return render(request, 'finderApp/recipe_detail.html', {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'recipe': recipe,
	})