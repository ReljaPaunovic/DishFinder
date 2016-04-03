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

from .models import Category
from .models import Ingredient
from .models import Direction
from .models import Recipe
from .models import Meal

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

	ingredient_list = []
	# load data
	data_url = 'finderApp/static/finderApp/data/ingredients_from_allrecipes.json'
	open(data_url, "r")
	with open(data_url) as data_file:
		ingredient_list = json.load(data_file)

	data_url = 'finderApp/static/finderApp/data/ingredients_BBC.json'
	open(data_url, "r")
	with open(data_url) as data_file:
		tmp_list = json.load(data_file)

	ingredient_list += tmp_list

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
		print(result_id_list[i][0])
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
	current_recipe = get_object_or_404(Recipe, pk=recipe_id)

	if request.method == 'POST':
		user_rating = request.POST['rating']
		current_user = request.user
		if request.user.is_authenticated():
			print()


	# retrieve list of recipe id which goes well with current recipe
	category_list = Category.objects.all()
	recipe_in_meal_list = []
	meal_set = Meal.objects.all().filter(suggestion__pk=recipe_id)
	for meal in meal_set:
		for recipe in meal.suggestion.all():
			if int(recipe.pk) != int(recipe_id):
				recipe_in_meal_list.append(recipe)

	tmp_meal_suggestion = []
	# initialize
	for i in range(len(category_list)):
		tmp_meal_suggestion.append({"cat_name":category_list[i].name,
								"cat_html_id": category_list[i].name.replace(" ", ""),
								"recipes":[]})

	for recipe in recipe_in_meal_list:
		if recipe not in tmp_meal_suggestion[recipe.category.pk - 1]["recipes"]:
			tmp_meal_suggestion[recipe.category.pk - 1]["recipes"].append(recipe)

	meal_suggestion = []
	for i in range(len(tmp_meal_suggestion)):
		if tmp_meal_suggestion[i]["recipes"]:
			meal_suggestion.append(tmp_meal_suggestion[i])

	return render(request, 'finderApp/recipe_detail.html', {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'recipe': current_recipe,
		'meal_suggestion': meal_suggestion,
	})

def add_recipe(request):
	login_err = login_service(request)['err_msg']
	category_list = Category.objects.all()

	if request.method == 'POST':
		recipe_name = request.POST['dish_name']
		category_id = request.POST['category']
		category = category_list[int(category_id) - 1]
		serving_num = request.POST['serve_num']
		image_url = ""
		current_user = request.user

		input_ingredients = request.POST['ingredientlist']
		input_ingredient_list = input_ingredients.split('\n')
		input_directions = request.POST['direction']
		input_direction_list = input_directions.split('\n')

		# create list of ingredient objects
		ingredient_list = []
		for i in range(len(input_ingredient_list)):
			if (input_ingredient_list[i] != ""):
				ingredient = Ingredient.objects.create(ingredient_name=input_ingredient_list[i])
				ingredient_list.append(ingredient.pk)

		# create list of direction objects
		direction_list = []
		for i in range(len(input_direction_list)):
			if (input_direction_list[i] != ""):
				direction = Direction.objects.create(recipe_direction=input_direction_list[i])
				direction_list.append(direction.pk)

		# add new recipe into DB
		recipe = Recipe()
		recipe.name = recipe_name
		recipe.image = image_url 
		recipe.servings = serving_num 
		recipe.category = category 
		recipe.creater = current_user
		recipe.save()
		for ingredient in ingredient_list:
			recipe.contained_ingredients.add(ingredient)
		for direction in direction_list:
			recipe.directions.add(direction)
		recipe.save()

		# update inverted index list for searching
		updateIndexList(input_ingredient_list)
		
	return render(request, 'finderApp/add_recipe.html', {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'category_list': category_list,
	})
