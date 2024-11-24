from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.text import slugify

import secrets

# Create your models here.
class Staff(models.Model):

	GENDER_CHOICES_MALE = 'M'
	GENDER_CHOICES_FEMALE = 'F'
	GENDER_CHOICES=[
	(GENDER_CHOICES_MALE,'MALE'),
	(GENDER_CHOICES_FEMALE,'FEMALE'),
	]
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="staff")
	phone_number = models.CharField(max_length=20)
	gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
	user_type = models.CharField(max_length=255,default='STAFF')
	shop_name = models.CharField(max_length=255)

	def __str__(self):

		return f'{self.user.username}'



class Collection(models.Model):
	title = models.CharField(max_length=255)

	def __str__(self):
		return f'{self.title}'

class Product(models.Model):
	product_id = models.CharField(max_length=255,primary_key=True)
	name = models.CharField(max_length=255,verbose_name='Product Name')
	description = models.TextField(verbose_name="Product Description")
	price = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(1)])
	slug= models.SlugField()
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE,related_name='products')
	quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
	at_created = models.DateTimeField(auto_now=True)
	at_updated = models.DateTimeField(auto_now_add=True)
	image= models.ImageField(upload_to='store/image',null=True,blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,null=True)

	def save(self,*args,**kwargs):
		while not self.product_id:
			product_id = 'PR_' + f'{secrets.token_hex(2)}'.upper()

			check_product_id = Product.objects.filter(product_id=product_id)

			if not check_product_id:
				self.product_id = product_id

		self.slug = slugify(self.name)

		super().save(*args,**kwargs)
		

	def __str__(self):
		return f'{self.name}'


class OrderItem(models.Model):

	collection = models.ForeignKey(Collection, on_delete=models.SET_NULL,null=True)
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	price = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(1)])
	quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
	order = models.ForeignKey('Order', on_delete=models.CASCADE,related_name="orderitems")

	def __str__(self):
		return f'{self.product.name}'


class Order(models.Model):
	order_id = models.CharField(max_length=255,primary_key=True)
	total_price = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(1)] , null=True)
	is_ordered = models.BooleanField(default=False)
	at_ordered = models.DateField(auto_now_add=True)
	items = models.ManyToManyField(OrderItem,related_name='items') 
	staff = models.ForeignKey(Staff, on_delete=models.SET_NULL,null=True)


	def save(self,*args,**kwargs):

		while not self.order_id:
			order_id = f'{secrets.token_hex(3)}'.upper()

			check_order_id = Order.objects.filter(order_id=order_id)

			if not check_order_id:

				self.order_id = order_id
		super().save(*args,**kwargs)


	def __str__(self):
		return f'{self.order_id}'




class OrderProduct(models.Model):
	order_id = models.CharField(max_length=255,primary_key=True)
	collection= models.ForeignKey(Collection, on_delete=models.PROTECT)
	product= models.ForeignKey(Product,on_delete=models.PROTECT)
	price = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(1)])
	total_price = models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(1)])
	quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
	at_ordered = models.DateField(auto_now_add=True)


	def save(self,*args,**kwargs):

		while not self.order_id:
			order_id = f'#{secrets.token_hex(3)}'.upper()

			check_order_id = OrderProduct.objects.filter(order_id=order_id)

			if not check_order_id:

				self.order_id = order_id
		super().save(*args,**kwargs)


	def __str__(self):
		return f'{self.product.name}'
		