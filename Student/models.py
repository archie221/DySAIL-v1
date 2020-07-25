from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class gadget(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.CharField(max_length=15)
	company = models.CharField(max_length=20)
	price = models.PositiveIntegerField(default=0,blank=True)
	image = models.ImageField(upload_to='gadgets')
	taken = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.company} {self.item}'

	def save(self):
		super().save()

		img = Image.open(self.image.path)
		output_size = (100, 120)
		img.thumbnail(output_size)
		img.save(self.image.path)

class chat(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	receiver = models.CharField(max_length=10)
	noted = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.sender.username}-{self.receiver}'

class messenger(models.Model):
	link = models.ForeignKey(chat, on_delete=models.CASCADE)
	send = models.BooleanField(default=False)
	message = models.CharField(max_length=1000)
	first = models.BooleanField(default=False)
	def __str__(self):
		return f'{self.link.sender.username}-{self.link.receiver}'

class chat_unseen(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f'{self.user.username} unseen chat count'




	
