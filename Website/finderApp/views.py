from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from django.template import RequestContext

from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

from .models import Ingredient
from .models import Direction
from .models import Recipe

from finderApp.login_service import login_service
from finderApp.rank_recipes import getSortedRecipes
from finderApp.rank_recipes import updateIndexList
from finderApp.form import UserCreationForm


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
	login_err = login_service(request)['err_msg']
	category_list = [{"name":"Appetizer", "id":0}, 
					 {"name":"Soup", "id":1}, 
					 {"name":"Main Dish", "id":2}, 
					 {"name":"Side Dish", "id":3}, 
					 {"name":"Dessert", "id":4}, 
					 {"name":"Salad", "id":5}]

	if request.method == 'POST':
		recipe_name = request.POST['dish_name']
		category = request.POST['category']
		serving_num = request.POST['serve_num']
		image_url = ""
		current_user = request.user

		input_ingredients = request.POST['ingredientlist']
		input_ingredient_list = input_ingredients.split('\\n')
		input_directions = request.POST['direction']
		input_direction_list = input_directions.split('\\n')

		# create list of ingredient objects
		ingredient_list = []
		for i in range(len(input_ingredient_list)):
			ingredient = Ingredient.objects.create(ingredient_name=input_ingredient_list[i])
			ingredient_list.append(ingredient.pk)

		# create list of direction objects
		direction_list = []
		for i in range(len(input_direction_list)):
			direction = Direction.objects.create(ingredient_name=input_direction_list[i])
			direction_list.append(ingredient.pk)

		# add new recipe into DB
		recipe = Recipe(name=recipe_name, image=image_url, category=category, servings=serving_num, creater=current_user)
		recipe.contained_ingredients.add(ingredient)
		recipe.directions.add(direction)
		recipe.save()

		# update inverted index list for searching
		updateIndexList(input_ingredients)
		
	return render(request, 'finderApp/add_recipe.html', {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'category_list': category_list,
	})
