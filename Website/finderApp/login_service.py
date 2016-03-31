from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

def login_service(request):
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
					is_loggedin = True
				else:
					err_msg = "disabled acc"
			else:
				err_msg = "invalid login"
	return {"status": is_loggedin, "err_msg": err_msg}