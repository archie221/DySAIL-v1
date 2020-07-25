from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class seats(models.Model):
	seatname = models.CharField(max_length=5)
	status = models.PositiveIntegerField(default=0)
	owner = models.CharField(max_length=50,blank=True)
	owner_roll = models.CharField(max_length=9,blank=True)
	idled_till = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
	hide = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.seatname}'

class bookseats(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	seatbooked = models.CharField(max_length=5)
	status = models.PositiveIntegerField(default=0)
	hide = models.BooleanField(default=False)
	other = models.BooleanField(default=False)
	leader = models.CharField(max_length=9)
	amount = models.PositiveIntegerField(default=0)
	expiry_time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
	alert_time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
	idletime = models.PositiveIntegerField(default=0)
	overnight = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user.username} booking'

class multipleseats(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Roll_No = models.CharField(max_length=9)
	clubbed = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user.username}-{self.Roll_No}'

class notification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.PositiveIntegerField(default=0)
	name = models.CharField(max_length=50)
	roll = models.CharField(max_length=9)
	seatname = models.CharField(max_length=5)
	time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

	def __str__(self):
		return f'{self.user.username} notification' 

class new_notes(models.Model): 
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f'{self.user.username} new notes'




