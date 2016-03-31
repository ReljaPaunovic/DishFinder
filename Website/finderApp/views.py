from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import auth
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
			return HttpResponseRedirect("/finder/")
	else:
		form = UserCreationForm()
	return render(request, 'finderApp/signup.html', {'form': form})

def login(request):
	is_loggedin = False
	err_msg = ""
	if request.method == "POST":
		if 'login' in request.POST:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					# Redirect to a success page.
					is_loggedin = True
				else:
					# Return a 'disabled account' error message
					err_msg = "disabled acc"
			else:
				# Return an 'invalid login' error message.
				err_msg = "invalid login"
	return {"status": is_loggedin, "err_msg": err_msg}
	# c = {'form':forms.Form}
	# c.update(csrf(request))
	# return render_to_response('finderApp/login.html', c)

def logout(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/finder/")

def index(request):
	login_err = login(request)['err_msg']
	print(login_err)
	# login_result = login(request)
	ingredient_list = Ingredient.objects.all()
	template = loader.get_template('finderApp/index.html')
	context = {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'ingredient_list': ingredient_list,
	}
	return HttpResponse(template.render(context, request))

def search_result(request):
	login_err = login(request)['err_msg']
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
	login_err = login(request)['err_msg']
	recipe = get_object_or_404(Recipe, pk=recipe_id)
	return render(request, 'finderApp/recipe_detail.html', {
		'is_auth':request.user.is_authenticated(),
		'login_err': login_err,
		'recipe': recipe,
	})