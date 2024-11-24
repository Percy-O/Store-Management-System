from accounts import models
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):

	class Meta():
		model = models.User
		fields=['first_name','last_name','username','email','password1','password2']


# class StaffForm(forms.ModelForm):

# 	class Meta():
# 		model = models.Staff
# 		fields = ['gender','user_type','phone_number','shop_name']