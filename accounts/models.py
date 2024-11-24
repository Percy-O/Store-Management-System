from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
	email = models.EmailField(max_length=255,unique=True)

# class Staff(models.Model):

# 	GENDER_CHOICES_MALE = 'M'
# 	GENDER_CHOICES_FEMALE = 'F'
# 	GENDER_CHOICES=[
# 	(GENDER_CHOICES_MALE,'MALE'),
# 	(GENDER_CHOICES_FEMALE,'FEMALE'),
# 	]
# 	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="staff")
# 	phone_number = models.CharField(max_length=20)
# 	gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
# 	user_type = models.CharField(max_length=255,default='STAFF')
# 	shop_name = models.CharField(max_length=255)

# 	def __str__(self):

# 		return f'{self.user.username}'

