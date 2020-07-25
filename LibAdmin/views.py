from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import key, searchform, studentgadgetform, studentbookform, idletimeform
from django.views.generic import TemplateView
from django.forms import formset_factory
from django.contrib import messages
from .models import authenticate, book_student, timedetails
from seatbooking.models import bookseats,seats
from Student.models import gadget
from django.contrib.auth.models import User
from seatbooking.views import notify
from django.utils import timezone
import datetime

auth = get_object_or_404(authenticate)

class passkeyView(TemplateView):
	template_name = 'LibAdmin/login.html'

	def get(self, request):
		if auth.login == True:
			auth.login = False
			auth.save()
		l_form = key()
		return render(request, self.template_name, {'l_form':l_form, 'flag':auth.login})	
	
	def post(self, request):
		form = key(request.POST)
		passkey = request.POST.get('passkey')
		if passkey == 'kgplib2020' :
			auth.login = True
			auth.save()
			return redirect('student-search')
		else :
			messages.error(request, f'Wrong Passkey!')
			return redirect('lib-login')
		return render(request, self.template_name, {'l_form':form, 'flag':auth.login})	

def logout(request):
	if auth.login == True:
		auth.login = False
		auth.save()
		return redirect('lib-login')
	else:
		messages.error(request, f'Login Required!')
		return redirect('lib-login')

def search(request):
	if auth.login == True:
		if request.method =='POST':
			s_form = searchform(request.POST)
			if s_form.is_valid():
				roll = request.POST.get('Roll_No')
				if len(roll) != 9:
					messages.error(request, f'Roll No should be exactly of 9 characters!')
					return redirect('student-search')
				student = get_object_or_404(User, username=roll)
				notify(student)
				student_booking = bookseats.objects.get(user=student)
				if student_booking.status == 0:
					messages.error(request, f'Booking N/A!') 
					return redirect('student-search')
				elif student_booking.status == 1:
					return HttpResponseRedirect(reverse("student-info", args=(student.username,)))
				elif student_booking.status == 2:
					return HttpResponseRedirect(reverse("student-occupied", args=(student.username,)))
				elif student_booking.status == 3:
					return HttpResponseRedirect(reverse("student-occupied", args=(student.username,)))
		else:
			s_form = searchform()
		return render(request, 'LibAdmin/search.html', {'s_form':s_form, 'flag':auth.login})
	else:
		messages.error(request, f'Login Required!')
		return redirect('lib-login')

def info_student(request,student_roll):
	if auth.login == True:
		student = get_object_or_404(User, username=student_roll)
		student_booking = bookseats.objects.get(user=student)
		seat = seats.objects.get(seatname=student_booking.seatbooked)
		gadget_count = gadget.objects.filter(user=student).count()
		gadget_student = gadget.objects.filter(user=student)
		try:
			book = book_student.objects.get(student=student)
		except book_student.DoesNotExist:
			book = book_student(student=student,book='None')
			book.save()
		GadgetFormSet = formset_factory(studentgadgetform,max_num=gadget_count,extra=gadget_count)
		if request.method =='POST':
			formset = GadgetFormSet(request.POST)
			if formset.is_valid():
				for form,gadgets in zip(formset,gadget_student):
					taken = form.cleaned_data.get('gadget_taken')
					if taken == True:
						gadgets.taken = taken
						gadgets.save()
					else:
						gadgets.taken = False
						gadgets.save()
			b_form = studentbookform(request.POST,instance=book)
			if b_form.is_valid():
				b_form.save()
			if student_booking.status == 1:
				student_booking.status = 2
				student_booking.save()
				seat.status = 2
				seat.save()
				time = timezone.now()
				try:
					checktimes = timedetails.objects.get(student=student,category=1)
				except timedetails.DoesNotExist:
					checktimes = timedetails(student=student,category=1,time=time)
					checktimes.save()
				messages.success(request, f'Booking Confirmed')
				return redirect('student-search')
			else:
				messages.success(request, f'Changes Saved')
				return HttpResponseRedirect(reverse("student-occupied", args=(student.username,)))
		b_form = studentbookform(instance=book)
		formset = GadgetFormSet()
		zipped = zip(formset,gadget_student)
		context={
					'student': student,
					'student_booking':student_booking,
					'gadget_count':gadget_count,
					'zipped':zipped,
					'b_form':b_form, 
					'flag': auth.login,
					'formset':formset
		}
		return render(request, 'LibAdmin/detail.html', context)
	else:
		messages.error(request, f'Login Required!')
		return redirect('lib-login')

def occupied_student(request,student_roll):
	if auth.login == True:
		student = get_object_or_404(User, username=student_roll)
		student_booking = bookseats.objects.get(user=student)
		gadgets = gadget.objects.filter(user=student)
		gadget_count = gadget.objects.filter(user=student,taken=True).count()
		book = book_student.objects.get(student=student)
		checktimes = timedetails.objects.filter(student=student)
		context={
					'student_roll':student_roll,
					'gadgets': gadgets,
					'book': book,
					'flag': auth.login,
					'gadget_count':gadget_count,
					'booking':student_booking,
					'checktimes':checktimes
		}
		return render(request, 'LibAdmin/occupied.html',context)
	else:
		messages.error(request, f'Login Required!')
		return redirect('lib-login') 
	
def idle_student(request,student_roll):
	if auth.login == True:
		student = get_object_or_404(User, username=student_roll)
		student_booking = bookseats.objects.get(user=student)
		seat = seats.objects.get(seatname=student_booking.seatbooked)
		if student_booking.overnight == True:
			student_booking.overnight = False
			student_booking.save()
		check_time = (timezone.now() + timezone.timedelta(hours=5,minutes=30)).time()
		flag1 = False
		if check_time >= datetime.time(0,0,0) and check_time <= datetime.time(6,0,0):
			flag1 = True
		if request.method =='POST':
			i_form = idletimeform(request.POST)
			if i_form.is_valid():
				mins = i_form.cleaned_data.get('minutes')
				time = timezone.now()
				student_booking.expiry_time = time + timezone.timedelta(minutes=mins)
				mins1 = mins - 10
				student_booking.alert_time = time + timezone.timedelta(minutes=mins1)
				student_booking.status = 3
				student_booking.idletime = mins
				student_booking.save()
				seat.status = 3
				mins2 = mins + 30
				seat.idled_till = time + timezone.timedelta(hours=5,minutes=mins2)
				seat.save()
				checktimes = timedetails(student=student,category=2,time=time)
				checktimes.save()
				messages.success(request, f'Successfully Idled!')
				return redirect('student-search')
		else:
			i_form = idletimeform()
		return render(request, 'LibAdmin/idle.html', {'i_form':i_form, 'flag':auth.login, 'flag1':flag1,'student_roll':student_roll})
	else:
		messages.error(request, f'Login Required!')
		return redirect('lib-login')

def idle_overnight(request,student_roll):
	if auth.login == True:
		student = get_object_or_404(User, username=student_roll)
		student_booking = bookseats.objects.get(user=student)
		seat = seats.objects.get(seatname=student_booking.seatbooked)
		time = timezone.now()
		student_booking.status = 3
		student_booking.expiry_time = time + timezone.timedelta(hours=9)
		student_booking.alert_time = time + timezone.timedelta(hours=8,minutes=50)
		student_booking.overnight = True
		student_booking.save()
		seat.status = 3
		seat.idled_till = time + timezone.timedelta(hours=14,minutes=30)
		seat.save()
		checktimes = timedetails(student=student,category=2,time=time)
		checktimes.save()
		messages.success(request, f'Successfully Idled Overnight!')
		return redirect('student-search')
	else:
		messages.error(request, f'Login Required!')
		return redirect('lib-login')

def overidle_student(request,student_roll):
	if auth.login == True:
		time = timezone.now()
		student = get_object_or_404(User, username=student_roll)
		student_booking = bookseats.objects.get(user=student)
		seat = seats.objects.get(seatname=student_booking.seatbooked)
		student_booking.status = 2
		student_booking.save()
		seat.status = 2
		seat.save()
		checktimes = timedetails(student=student,category=3,time=time)
		checktimes.save()
		messages.success(request, f'Idling Terminated')
		return redirect('student-search')
	else:
		messages.error(request, f'Login Required!')
		return redirect('lib-login')

def terminate_student(request,student_roll):
	if auth.login == True:
		student = get_object_or_404(User, username=student_roll)
		student_booking = bookseats.objects.get(user=student)
		seat = seats.objects.get(seatname=student_booking.seatbooked)
		timedetails.objects.filter(student=student).delete()
		book = book_student.objects.get(student=student)
		book.book = 'None'
		book.save()
		student_booking.status = 0
		student_booking.save()
		seat.status = 0
		seat.save()
		messages.success(request, f'Booking Terminated')
		return redirect('student-search')
	else:
		messages.error(request, f'Login Required!')
		return redirect('lib-login')



