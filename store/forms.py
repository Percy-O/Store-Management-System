from django import forms
from store import models

class CollectionForm(forms.ModelForm):

	class Meta:

		model  = models.Collection
		fields = ['title']

class ProductForm(forms.ModelForm):

	class Meta:

		model = models.Product
		fields = ['name','description','collection','price','quantity']

class OrderProductForm(forms.ModelForm):

	total_price = forms.DecimalField(label="")
	class Meta:

		model = models.OrderProduct
		fields = ['collection','product','quantity','price','total_price']


	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['product'].queryset = models.Product.objects.none()
		self.fields['quantity'].widget = forms.TextInput(attrs={'id':'quantity','type':'number'})
		self.fields['price'].widget = forms.TextInput(attrs={'id':'price'})
		self.fields['total_price'].widget = forms.TextInput(attrs={'id':'total_price','type':'number'})
		self.fields['price'].widget.attrs['hidden'] = True
		self.fields['total_price'].widget.attrs['hidden'] = True

		# Create
		if 'collection' in self.data:
			try:
				collection_id = int(self.data.get('collection'))
				self.fields['product'].queryset = models.Product.objects.filter(collection_id=collection_id).order_by('name')
			except (ValueError,TypeError):
				pass
		elif 'product' in self.data:

			try: 
				product_id = self.data.get('product')
				self.fields['price'].queryset = models.Product.objects.get(product_id = product_id).values('price')
			except (ValueError,TypeError):
				pass

		# Update
		elif self.instance.pk:
			self.fields['product'].queryset = self.instance.collection.products.order_by('name')


class OrderItemForm(forms.ModelForm):

	total_price = forms.DecimalField(label="")
	class Meta:

		model = models.OrderItem
		fields = ['collection','product','quantity','price']


	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['product'].queryset = models.Product.objects.none()
		self.fields['collection'].queryset = models.Collection.objects.all().distinct()
		self.fields['quantity'].widget = forms.TextInput(attrs={'id':'quantity','type':'number'})
		self.fields['price'].widget = forms.TextInput(attrs={'id':'price'})
		self.fields['total_price'].widget = forms.TextInput(attrs={'id':'total_price','type':'number'})
		self.fields['price'].widget.attrs['hidden'] = True
		
		
		# Create
		if 'collection' in self.data:
			try:
				collection_id = int(self.data.get('collection'))
				self.fields['product'].queryset = models.Product.objects.filter(collection_id=collection_id).order_by('name')
			except (ValueError,TypeError):
				pass
		elif 'product' in self.data:

			try: 
				product_id = self.data.get('product')
				self.fields['price'].queryset = models.Product.objects.get(product_id = product_id).values('price')
			except (ValueError,TypeError):
				pass

		# Update
		elif self.instance.pk:
			self.fields['product'].queryset = self.instance.collection.products.order_by('name')


class StaffForm(forms.ModelForm):

	class Meta():
		model = models.Staff
		fields = ['gender','user_type','phone_number','shop_name']