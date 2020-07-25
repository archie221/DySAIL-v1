from django.shortcuts import render,redirect
import json
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.forms import formset_factory
from .forms import extraseats,multiplebook_ids
from .models import seats,bookseats,multipleseats,notification,new_notes
from LibAdmin.models import book_student, timedetails
from Student.models import gadget
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone


def notify(user1):
	time = timezone.now()
	bookseat = bookseats.objects.get(user=user1)
	unseen = new_notes.objects.get(user=user1)
	if bookseat.status == 1:
		if bookseat.alert_time < time:
			try:
				notice1 = notification.objects.get(user=user1,category=1,time=bookseat.alert_time,seatname=bookseat.seatbooked)
			except notification.DoesNotExist:
				notice = notification(user=user1,category=1,time=bookseat.alert_time,seatname=bookseat.seatbooked)
				notice.save()
				unseen.count = unseen.count + 1
				unseen.save()
		if bookseat.expiry_time < time:
			notice = notification(user=user1,category=2,time=bookseat.expiry_time,seatname=bookseat.seatbooked)
			notice.save()
			unseen.count = unseen.count + 1
			unseen.save()
			bookseat.status = 0
			bookseat.amount = 0
			bookseat.save()
	elif bookseat.status == 3:
		if bookseat.alert_time < time:
			try:
				notice1 = notification.objects.get(user=user1,category=3,time=bookseat.alert_time,seatname=bookseat.seatbooked)
			except notification.DoesNotExist:
				notice = notification(user=user1,category=3,time=bookseat.alert_time,seatname=bookseat.seatbooked)
				notice.save()
				unseen.count = unseen.count + 1
				unseen.save()
		if bookseat.expiry_time < time:
			notice = notification(user=user1,category=4,time=bookseat.expiry_time,seatname=bookseat.seatbooked)
			notice.save()
			unseen.count = unseen.count + 1
			unseen.save()
			bookseat.status = 0
			bookseat.amount = 0
			bookseat.save()
	return
		

def seatview(request):
	time = timezone.now()
	seat1 = seats.objects.filter(status=1)
	for x in seat1:
		user2 = User.objects.get(username=x.owner_roll)
		bookseat = bookseats.objects.get(user=user2)
		if bookseat.seatbooked == x.seatname:
			if bookseat.expiry_time < time:
				x.status = 0;
				x.save()
		else:
			x.status = 0;
			x.save()
	seat2 = seats.objects.filter(status=3)
	for y in seat2:
		user2 = User.objects.get(username=y.owner_roll)
		bookseat = bookseats.objects.get(user=user2)
		if bookseat.seatbooked == y.seatname:
			if bookseat.expiry_time < time:
				y.status = 0;
				y.save()
		else:
			y.status = 0;
			y.save()
	seat = seats.objects.all()
	user1 = request.user
	if user1.is_authenticated:
		notify(user1)
		bookseat = bookseats.objects.get(user=user1)
		flag = True
		if bookseat.other == True and bookseat.leader == user1.username:
			multipleseat = multipleseats.objects.filter(user=user1,clubbed=True)
			for multiseat in multipleseat:
				user2 = User.objects.get(username=multiseat.Roll_No)
				notify(user2)
				bookseat2 = bookseats.objects.get(user=user2)
				if bookseat2.status != 0:
					flag = False
		count = bookseat.amount + 1
		return render(request,'seatbooking/view.html',{'seats':seat,'count':count,'bookseat':bookseat,'flag':flag})
	else:
		return render(request,'seatbooking/view.html',{'seats':seat})

@login_required

def book(request):
	user1 = request.user
	notify(user1)
	time = timezone.now()
	if request.is_ajax and request.method == "POST":
		seatnames = []
		seatnames = request.POST.getlist('seat_ids[]')
		for y in range(len(seatnames)):
			seat_id = seats.objects.get(seatname=seatnames[y])
			if seat_id.status != 0:
				return HttpResponse('{"status":"fail"}', content_type='application/json')
		bookseat = bookseats.objects.get(user=user1)
		bookseat.seatbooked = seatnames[0]
		bookseat.status = 1
		bookseat.expiry_time = time + timezone.timedelta(minutes=30)
		bookseat.alert_time = time + timezone.timedelta(minutes=20)
		bookseat.save()
		my_seat = seats.objects.get(seatname=seatnames[0])
		my_seat.status = 1
		my_seat.owner_roll = user1.username
		my_seat.owner = user1.first_name + ' ' + user1.last_name
		my_seat.hide = bookseat.hide
		my_seat.save()
		if len(seatnames) > 1:
			clubbed_rolls = multipleseats.objects.filter(user=user1,clubbed=True)
			x = 1
			for clubbed_roll in clubbed_rolls:
				clubbed_user = User.objects.get(username=clubbed_roll.Roll_No)
				multiseat = bookseats.objects.get(user=clubbed_user)
				multiseat.seatbooked = seatnames[x]
				multiseat.status = 1
				multiseat.expiry_time = time + timezone.timedelta(minutes=30)
				multiseat.alert_time = time + timezone.timedelta(minutes=20)
				multiseat.save()
				seat = seats.objects.get(seatname=seatnames[x])
				seat.status = 1
				seat.owner_roll = clubbed_user.username
				seat.owner = clubbed_user.first_name + ' ' + clubbed_user.last_name
				seat.hide = multiseat.hide
				seat.save()
				x = x+1 
		return HttpResponse('{"status":"success"}', content_type='application/json')
	else:
		return HttpResponse('{"status":"fail"}', content_type='application/json')


def booking(request):
	user1 = request.user
	notify(user1)
	bookseat = bookseats.objects.get(user=user1)
	extraseat_count = multipleseats.objects.filter(user=user1).count()
	flag = True
	if bookseat.other == True and bookseat.leader == user1.username:
		multipleseat = multipleseats.objects.filter(user=user1,clubbed=True)
		for multiseat in multipleseat:
			user2 = User.objects.get(username=multiseat.Roll_No)
			notify(user2)
			bookseat2 = bookseats.objects.get(user=user2)
			if bookseat2.status != 0:
				flag = False
	return render(request,'seatbooking/book.html',{'bookseats':bookseat,'extraseat_count':extraseat_count,'flag':flag})

def multipleseat(request):
	user1 = request.user
	multipleseats.objects.filter(user=user1).delete()
	bookseat = bookseats.objects.get(user=user1)
	bookseat.amount = 0
	bookseat.save()
	if request.method =='POST':
		form = extraseats(request.POST,instance=bookseat)
		if form.is_valid():
			form.save()
			return redirect('club-ids')
	else:
		form = extraseats()
	return render(request, 'seatbooking/multipleseat.html', {'form':form})

def club(request):
	user1 = request.user
	bookseat = bookseats.objects.get(user=user1)
	x = bookseat.amount
	ClubFormSet = formset_factory(multiplebook_ids,max_num=x,extra=x)
	if request.method =='POST':
		time = timezone.now()
		formset = ClubFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				username = form.cleaned_data.get('Roll_No')
				print(username)
				try:
					user2 = User.objects.get(username=username)
				except User.DoesNotExist:
					bookseat.amount = 0
					bookseat.save()
					messages.error(request, f'{username} is an Invalid Username. Book Again')
					return redirect('book-multiple')
				multiseat = bookseats.objects.get(user=user2)
				notify(user2)
				if multiseat.status != 0:
					bookseat.amount = 0
					bookseat.save()
					messages.error(request, f'{multiseat.user.username} has a seat booked already')
					return redirect('book-multiple')
				if multiseat.other == True:
					bookseat.amount = 0
					bookseat.save()
					messages.error(request, f'{multiseat.user.username} is clubbed with someone else')
					return redirect('book-multiple')
				if multipleseats.objects.filter(user=user1,Roll_No=username).exists():
					messages.error(request, f'You repeated Roll No.s in form filling')
					return redirect('book-multiple')
				multipleseat = multipleseats(user=user1,Roll_No=username)
				multipleseat.save()
				notice = notification(user=user2,category=5,name=user1.first_name + ' ' + user1.last_name,roll=user1.username,time=time)
				notice.save()
				unseen = new_notes.objects.get(user=user2)
				unseen.count = unseen.count + 1
				unseen.save()
		bookseat.amount = 0
		bookseat.save()
		return redirect('book-details')
	formset = ClubFormSet()
	return render(request, 'seatbooking/club.html', {'formset':formset,'bookseat':bookseat})

def yes_request(request,username):
	user1 = request.user
	notify(user1)
	user2 = User.objects.get(username=username)
	try:
		multiseat = multipleseats.objects.get(user=user2,Roll_No=user1.username)
	except multipleseats.DoesNotExist:
		notification.objects.filter(user=user1,category=5,roll=username).delete()
		messages.error(request, f'Request Expired!')
		return redirect('notices')
	bookseat = bookseats.objects.get(user=user1)
	if bookseat.other == True and bookseat.status != 0:
		messages.error(request, f'Cancel current booking and clubbing to allow other user to book for you!')
		return redirect('book-details')
	if bookseat.status != 0:
		messages.error(request, f'Cancel current booking to allow other user to book for you!')
		return redirect('book-details')
	if bookseat.other == True:
		messages.error(request, f'Cancel current clubbing to allow other user to club with you!')
		return redirect('book-details')
	bookseat.other = True
	bookseat.leader = username
	bookseat.save()
	bookseat1 = bookseats.objects.get(user=user2)
	bookseat1.other = True
	bookseat1.leader = username
	bookseat1.amount = bookseat1.amount + 1
	bookseat1.save()
	multiseat.clubbed = True
	multiseat.save()
	notification.objects.get(user=user1,category=5,roll=username).delete()
	if bookseat1.status != 0:
		messages.success(request, f'Clubbed Succesfully!')
		messages.error(request, f'Clubber has a booked seat already, he wont be able to book for you until he cancels his own booking!')
		return redirect('book-details')
	messages.success(request, f'Clubbed Succesfully!')
	return redirect('book-details')


def no_request(request,username):
	user1 = request.user
	notify(user1)
	notification.objects.get(user=user1,category=5,roll=username).delete()
	user2 = User.objects.get(username=username)
	try:
		multipleseats.objects.filter(user=user2,Roll_No=user1.username).delete()
	except multipleseats.DoesNotExist:
		messages.error(request, f'Request Expired!')
		return redirect('notices')
	return redirect('notices')

def end_club(request):
	user1 = request.user
	notify(user1)
	time = timezone.now()
	bookseat = bookseats.objects.get(user=user1)
	if bookseat.leader == user1.username and bookseat.other == True:
		multiseat = multipleseats.objects.filter(user=user1)
		for seatowners in multiseat:
			if seatowners.clubbed == True:
				user2 = User.objects.get(username=seatowners.Roll_No)
				bookseat1 = bookseats.objects.get(user=user2)
				bookseat1.other = False
				bookseat1.save()
				notice = notification(user=user2,category=6,name=user1.first_name + ' ' + user1.last_name,roll=user1.username,time=time) 
				notice.save()
				unseen = new_notes.objects.get(user=user2)
				unseen.count = unseen.count + 1
				unseen.save()
		multiseat.delete()
		bookseat.other = False
		bookseat.amount = 0
		bookseat.save()
		return redirect('book-details')
	elif bookseat.other == True:
		bookseat.other = False
		bookseat.save()
		user2 = User.objects.get(username=bookseat.leader)
		multipleseats.objects.filter(user=user2,Roll_No=user1.username).delete()
		bookseat1 = bookseats.objects.get(user=user2)
		bookseat1.amount = bookseat1.amount - 1
		bookseat1.save()
		if bookseat1.amount == 0:
			bookseat1.other = False
			bookseat1.save()
		messages.success(request, f'Clubbing Ended!')
		return redirect('book-details')
	else:
		messages.error(request, f'Clubbing Expired Already!')
		return redirect('book-details')

def cancel(request):
	user1 = request.user
	notify(user1)
	bookseat = bookseats.objects.get(user=user1)
	if bookseat.status == 1:
		bookseat.status = 0
		bookseat.save()
		seat = seats.objects.get(seatname=bookseat.seatbooked)
		seat.status = 0
		seat.save()
		messages.success(request, f'Booking Ended!')
		return redirect('book-details')
	elif bookseat.status == 3:
		gadgets = gadget.objects.filter(user=user1)
		lib_book = book_student.objects.get(student=user1)
		flag = True
		for tech in gadgets:
			if tech.taken == True:
				flag = False
				break
		if flag == True and lib_book.book == 'None':
			bookseat.status = 0
			bookseat.save()
			seat = seats.objects.get(seatname=bookseat.seatbooked)
			seat.status = 0
			seat.save()
			timedetails.objects.filter(student=user1).delete()
			messages.success(request, f'Booking Ended!')
			return redirect('book-details')
		else:
			messages.error(request, f'Invalid Request! Your belongings are still in library. Firstly check them out')
			return redirect('book-details')

def hide(request):
	user1 = request.user
	notify(user1)
	if request.is_ajax and request.method == "GET":
		bookseat = bookseats.objects.get(user=user1)
		if bookseat.hide == True:
			bookseat.hide = False
			bookseat.save()
			if bookseat.status != 0:
				seat = seats.objects.get(seatname=bookseat.seatbooked)
				seat.hide = False
				seat.save()
		else:
			bookseat.hide = True
			bookseat.save()
			if bookseat.status != 0:
				seat = seats.objects.get(seatname=bookseat.seatbooked)
				seat.hide = True
				seat.save()
	else:
		return HttpResponse('{"status":"fail"}', content_type='application/json')

				

				


