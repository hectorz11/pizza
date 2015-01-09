from django import forms
from pizza.apps.page.models import producto,carrito

class addProductForm(forms.ModelForm):
	class Meta:
		model 	= producto
		exclude	= {'status',}

class addCarritoForm(forms.ModelForm):
	class Meta:
		model 	= carrito