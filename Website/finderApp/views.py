from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

import json

from finderApp.form import UserCreationForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
# from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Ingredient
from .models import Recipe

from finderApp.login_service import login_service
from finderApp.rank_recipes import getSortedRecipes


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
	template = loader.get_template('finderApp/index.html')

	# load data
	data_url = 'finderApp/static/finderApp/data/ingredients_from_allrecipes.json'
	open(data_url, "r")
	with open(data_url) as data_file:
		ingredient_list = json.load(data_file)

	context = {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'ingredient_list': ingredient_list,
	}
	return HttpResponse(template.render(context, request))

def search_result(request):
	login_err = login_service(request)['err_msg']
	template = loader.get_template('finderApp/search_result.html')

	selected_ingredient_list = []
	if request.method == "GET":
		if 'ingredient_list' in request.GET:
			selected_ingredient_list_string = request.GET['ingredient_list']
			# json decode
			selected_ingredient_list = json.loads(selected_ingredient_list_string)

	# process selected_ingredient_list to calc result_id_list
	result_id_list = getSortedRecipes(selected_ingredient_list)

	result_list = []
	for i in range(len(result_id_list)):
		obj = Recipe.objects.get(pk=result_id_list[i][0])
		obj.index = result_id_list[i][0]
		result_list.append(obj)

	# Show 25 recipe per page
	paginator = Paginator(result_list, 10)
	page = request.GET.get('page')
	try:
		recipes = paginator.page(page)
	except PageNotAnInteger:
		# deliver first page
		recipes = paginator.page(1)
	except EmptyPage:
		# page out of range, deliver last page
		recipes = paginator.page(paginator.num_pages)

	context = {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'recipes': recipes,
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

def add_recipe(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
	else:
		form = UserCreationForm()
	return render(request, 'finderApp/add_recipe.html', {'form': form})
