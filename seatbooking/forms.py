from django import forms
from .models import bookseats,multipleseats

class extraseats(forms.ModelForm):
	class Meta:
		model = bookseats
		exclude = {'status'}
		fields = ['amount']

class multiplebook_ids(forms.Form):
	Roll_No = forms.CharField()