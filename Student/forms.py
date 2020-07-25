from django import forms
from .models import gadget

class gadgetform(forms.ModelForm):
	class Meta:
		model = gadget
		fields = ['item','company','price','image']
		exclude = {'taken','user','id'}
		help_texts = {'price':'Will be set to zero by default'}
		widgets = {
			'price': forms.NumberInput(attrs={'placeholder':'In Indian Currency'})
			}

class sendmessage(forms.Form):
	message = forms.CharField(max_length=1000,label='',widget= forms.TextInput(attrs={'placeholder':'Type your message here'}))

class receiver(forms.Form):
	Roll_No = forms.CharField(max_length=9, widget= forms.TextInput(attrs={'placeholder':'Enter the Roll No of person you want to chat with'}))



