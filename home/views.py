from django.shortcuts import render, get_object_or_404
from LibAdmin.models import authenticate
from django.contrib.auth import logout

def home(request):
	auth = get_object_or_404(authenticate)
	if request.user.is_authenticated:
		logout(request)
	return render(request,'home/home.html', {'flag':auth.login})
