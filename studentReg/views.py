from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from Student.models import chat,messenger

def register(request):
	if request.method =='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'studentReg/register.html', {'form': form})

@login_required
def profile(request):
	return render(request, 'studentReg/profile.html')

def update(request):
	if request.method =='POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		prev_username = request.user.username
		if u_form.is_valid(): 
			u_form.save()
			username = u_form.cleaned_data.get('username')
			chat1 = chat.objects.filter(receiver=prev_username)
			for chats in chat1:
				message1 = messenger.objects.filter(link=chats)
				chats.receiver = username
				chats.save()
				for message in message1:
					message.link = chats
					message.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)	
	context = {
		'u_form': u_form,
	}
	return render(request, 'studentReg/update.html', context)
