from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class authenticate(models.Model):
	login = models.BooleanField(default=False)

class book_student(models.Model):
	student = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.SlugField(max_length=100,blank=True)

	def __str__(self):
		return f'{self.student.username} Book'

class timedetails(models.Model):
	student = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.PositiveIntegerField(default=0)
	time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

	def __str__(self):
		return f'{self.student.username} Timedetails'
	