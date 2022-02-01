from django.forms import ModelForm
from store.models.orders import Order
from django.forms.widgets import HiddenInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models.product import Product
from django import forms

from store.models.models import Post

class OrderForm(ModelForm):
	class Meta:
		model=Order
		fields=('address','phone')

class ViewCartForm(forms.ModelForm):
	class Meta:
		model=Order
		fields=('quantity','id',)
	def __init__(self, *args, **kwargs,):
		super().__init__(*args, **kwargs)
		
		self.fields['quantity']=forms.FloatField(max_value=100, min_value=1)
class RegistrationForm(UserCreationForm):
	email=forms.EmailField()

	class Meta:
		model=User
		fields=["username","email","password1","password2"]




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
