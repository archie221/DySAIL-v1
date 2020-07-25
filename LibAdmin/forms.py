from django import forms
from .models import book_student

class key(forms.Form):
	passkey = forms.CharField(max_length=50)

class searchform(forms.Form):
	Roll_No = forms.CharField(max_length=15)

class studentgadgetform(forms.Form):
	gadget_taken = forms.BooleanField(label='',required=False)

class studentbookform(forms.ModelForm):
   	class Meta:
   		model = book_student
   		fields = ['book']
   		labels = {
   			'book':'' 
   		}

class idletimeform(forms.Form):
	minutes = forms.IntegerField(max_value=120,widget= forms.NumberInput(attrs={'placeholder':'(<120)'}),help_text='You cant idle your seat for more than 2 hours')



	

