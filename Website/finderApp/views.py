from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from .models import Ingredient
from .models import Recipe

import json

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/finderApp/")
	else:
		form = UserCreationForm()
	return render(request, 'finderApp/signup.html', {'form': form})

def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				# Redirect to a success page.
				print("logged in")
			else:
				# Return a 'disabled account' error message
				print("disabled acc")
		else:
			# Return an 'invalid login' error message.
			print("invalid login")
	c = {'form':forms.Form}
	c.update(csrf(request))
	return render_to_response('finderApp/login.html', c)

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