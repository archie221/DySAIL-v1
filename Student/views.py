from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.db import transaction, IntegrityError
from .forms import gadgetform,sendmessage,receiver
from .models import gadget,chat,chat_unseen,messenger
from seatbooking.models import bookseats,notification,new_notes
from django.contrib.auth.models import User
from seatbooking.views import notify
from django.contrib import messages

@login_required

def home(request):
	user1 = request.user
	try:
		chat_unseen1 = chat_unseen.objects.get(user=user1)
	except chat_unseen.DoesNotExist:
		chat_unseen1 = chat_unseen(user=user1)
		chat_unseen1.save()
	try:
		bookseat = bookseats.objects.get(user=user1)
	except bookseats.DoesNotExist:
		bookseat = bookseats(user=user1)
		bookseat.save()
	try:
		unseen = new_notes.objects.get(user=user1)
	except new_notes.DoesNotExist:
		unseen = new_notes(user=user1)
		unseen.save()
	notify(user1)
	return render(request, 'Student/home.html')

def gadgets(request):
	user1 = request.user
	notify(user1)
	gadget_count = gadget.objects.filter(user=user1).count()
	return render(request, 'Student/gadgets.html',{'gadget_count':gadget_count})

def updateGadget(request):
	user1 = request.user
	gadgetFormset = inlineformset_factory(User, gadget, form=gadgetform, extra=1)	
	if request.method == "POST":
		formset = gadgetFormset(request.POST, request.FILES, instance=user1)
		if formset.is_valid():
			formset.save()
			if 'btn1' in request.POST:
				return redirect('update_gadgets')
			elif 'btn2' in request.POST:
				return redirect('gadgets')
	formset = gadgetFormset(instance=user1)
	return render(request, 'Student/update_gadgets.html', {'formset':formset})

class chatView(TemplateView):
	template_name = 'Student/chat.html'

	def get(self, request):
		user1 = request.user
		notify(user1)
		chat_unseen1 = chat_unseen.objects.get(user=user1)
		chat_unseen1.count = 0
		chat_unseen1.save()
		chatnotes = chat.objects.filter(sender=user1,noted=True).count()
		r_form = receiver()
		return render(request, self.template_name, {'r_form':r_form, 'chatnotes':chatnotes})	
	
	def post(self, request):
		user1 = request.user
		form = receiver(request.POST)
		if form.is_valid():
			receive = request.POST.get('Roll_No')
			if receive == user1.username:
				messages.error(request, f'Sorry! Scientists are still trying to find a person exactly like you')
				return redirect('chat')
			user2 = get_object_or_404(User,username=receive)
			try:
				chat1 = chat.objects.get(sender=user1,receiver=user2.username)
			except chat.DoesNotExist:
				chat1 = chat(sender=user1,receiver=user2)
				chat1.save()
			try:
				chat2 = chat.objects.get(sender=user2,receiver=user1.username)
			except chat.DoesNotExist:
				chat2 = chat(sender=user2,receiver=user1)
				chat2.save()
			return HttpResponseRedirect(reverse("chatbox", args=(user2.username,)))
		return render(request, self.template_name, {'r_form':form, 'chatnotes':chatnotes})

class chatboxView(TemplateView):
	template_name = 'Student/chatbox.html'

	def get(self,request,receiver_username):
		user1 = request.user
		notify(user1)
		if receiver_username == user1.username:
			messages.error(request, f'Sorry! Scientists are still trying to find a person exactly like you')
			return redirect('chat')
		user2 = get_object_or_404(User,username=receiver_username)
		try:
				chat1 = chat.objects.get(sender=user1,receiver=user2.username)
				chat2 = chat.objects.get(sender=user2,receiver=user1.username)
		except chat.DoesNotExist:
				chat1 = chat(sender=user1,receiver=user2)
				chat1.save()
				chat2 = chat(sender=user2,receiver=user1)
				chat2.save()
		if chat1.noted == True:
			chat1.noted = False
			chat1.save()
		m_form = sendmessage()
		context={
					'chat':chat1,
					'm_form':m_form
		}
		return render(request, self.template_name, context)	
		
	def post(self,request,receiver_username):
		user1 = request.user
		form2 = sendmessage(request.POST)
		user2 = get_object_or_404(User,username=receiver_username)
		chat1 = chat.objects.get(sender=user1,receiver=user2.username)
		chat2 = chat.objects.get(sender=user2,receiver=user1.username)
		msg_count = messenger.objects.filter(link=chat1).count()
		flag = False
		if msg_count != 0:
			prev_msg = messenger.objects.filter(link=chat1)[msg_count-1]
			if prev_msg.send == False:
				flag = True
		else:
			flag = True
		context={
					'chat':chat1,
					'm_form':form2
		}
		if form2.is_valid():
			msg = request.POST.get('message')
			message1 = messenger(link=chat1,message=msg,send=True)
			message2 = messenger(link=chat2,message=msg)
			if flag == True:
				message1.first = True
				message2.first = True
			message1.save()
			message2.save()
			chat2.noted = True
			chat2.save()
			chat_unseen2 = chat_unseen.objects.get(user=user2)
			chat_unseen2.count = chat_unseen2.count + 1
			chat_unseen2.save()
			return HttpResponseRedirect(reverse("chatbox", args=(user2.username,))) 
		return render(request, self.template_name, context) 


def notifications(request):
	user1 = request.user	
	notify(user1)
	unseen = new_notes.objects.get(user=user1)
	unseen.count = 0
	unseen.save()
	notifications = notification.objects.filter(user=user1).order_by('-time')
	note_count = notification.objects.filter(user=user1).count()
	return render(request, 'Student/notification.html',{'notifications':notifications, 'note_count':note_count})

def notifications_delete(request):
	user1 = request.user
	notify(user1)
	for x in range(1,5):
		notification.objects.filter(user=user1,category=x).delete()
	notification.objects.filter(user=user1,category=6).delete()
	return redirect('notices') 
	


