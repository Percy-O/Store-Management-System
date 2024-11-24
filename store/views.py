from django.db import transaction
from django.db.models import F,Q,ExpressionWrapper
from django.db.models.aggregates import Count,Sum
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from django.utils.html import format_html

from fpdf import FPDF
from django.http import FileResponse


from store import forms,models
from accounts.models import User

# User = settings.AUTH_USER_MODEL

# Create your views here.

def dashboard(request):

	
	collections = models.Collection.objects.all()
	products = models.Product.objects.select_related('collection').all()

	complete = True
	pend = False

	completed_orders = models.Order.objects.filter(is_ordered=True)
	pending_orders = models.Order.objects.filter(is_ordered=False)



	context={
		'collections':collections,
		'products':products,
		'completed_orders':completed_orders,
		'pending_orders':pending_orders,
		'pend':pend,
		'complete':complete
	}
	return render(request,'store/dashboard.html',context)

def add_collection(request):

	products=None
	# product= models.Product.objects.values('id').distinct()
	collections= models.Collection.objects.all().annotate(product_assigned_to_collection=Count(F('products'))).distinct()
	form = forms.CollectionForm()

	collection_product = request.GET.get('collection_product')
	if request.method == 'GET' and collection_product != None :
		collection = request.GET.get('collection_product') if request.GET.get('collection_product') != None else ' '
		products = models.Product.objects.filter(collection__id=collection)

	if request.method == 'POST':
		form = forms.CollectionForm(data=request.POST)

		if form.is_valid():
			form.save()
			messages.success(request,'Collection Sucessfully Saved!')
			return HttpResponseRedirect('.')

		else:

			messages.error(request, 'Unable to Update Collection!')


	context={
				'form':form,
				'collections':collections,
				'products':products,
				'collection_product':collection_product
	}
	return render(request,'store/collection.html',context)


def update_collection(request,pk):

	verify = 'update'
	collection = models.Collection.objects.get(pk=pk)
	form = forms.CollectionForm(instance=collection)

	if request.method == 'POST':

		title = request.POST.get('title')

		collection.title = title

		collection.save()

		if collection:

			messages.success(request, 'Collection Updated Successfully!')
			return redirect('store:collection')
		else:

			messages.error(request, 'Unable to Update Collection!')

		return redirect('store:collection')

	context = {'form':form,'verify':verify}
	return render(request, 'store/collection.html',context)


def delete_collection(request,pk):

	collection = models.Collection.objects.get(pk=pk)

	if request.method == 'POST':

		collection.delete()

		if collection:

			messages.success(request, 'Collection Successfully Deleted!')
			return redirect('store:collection')
		else:

			messages.error(request, 'Unable to Update Collection!')

		return redirect('store:collection')


	context = {'obj':collection}
	return render(request, 'store/delete.html',context)


def all_product(request):

	products = models.Product.objects.select_related('collection').all()

	context={'products':products}
	return render(request, 'store/products.html',context)
	
def add_product(request):


	collections = models.Collection.objects.all()
	if request.method == 'GET':
		form = forms.ProductForm()

	elif request.method =='POST':
		with transaction.atomic():
			# Getting Collection From the Form
			collection_title = request.POST.get('collection')

			# Get or Create Collection
			product_collection,created = models.Collection.objects.get_or_create(title=collection_title)

			#  Getting the Product Info From the Form

			product_name = request.POST.get('name')
			product_description = request.POST.get('description')
			product_price = request.POST.get('price')
			product_quantity = request.POST.get('quantity')
			product_user = request.user

			if models.Product.objects.filter(name=product_name).exists():
				messages.warning(request,'Product Name Exist!')
				return HttpResponseRedirect('.')


			else:
				# Create a Product
				models.Product.objects.create(

					user = product_user,
					quantity = product_quantity,
					price = product_price,
					description = product_description,
					name = product_name,
					collection =  product_collection
				)
				messages.success(request, 'Product Saved Successfully!')

				return HttpResponseRedirect('.')

		
	context = {
				'form':form,
				'collections':collections
	}

	return render(request, 'store/product.html',context)


def update_product(request,slug):

	verify = 'update'
	collections = models.Collection.objects.all()
	product = models.Product.objects.get(slug=slug)
	collection_get = product.collection.title
	form = forms.ProductForm(instance=product)

	if request.method == 'POST':

		# Get Product
		product_name = request.POST.get('name')
		product_description = request.POST.get('description')
		product_price = request.POST.get('price')
		product_quantity = request.POST.get('quantity')

		# Get Collection
		collection = request.POST.get('collection')
		product_collection,created = models.Collection.objects.get_or_create(title=collection.strip())

		# Update Product Instance
		product.name = product_name
		product.description = product_description
		product.price = product_price
		product.quantity = product_quantity
		product.collection = product_collection
		product.save()

		if product:
			messages.success(request, 'Product Updated Successfully!')
			return redirect('store:products')
		else:
			messages.error(request, 'Product Unable to Updated!')
		
		return redirect('store:products')


	context = {
				'form':form,
				'collections':collections,
				'verify':verify,
				'collection':collection_get}

	return render(request,'store/product.html',context)


def delete_product(request,slug):

	
	product = models.Product.objects.get(slug=slug)

	if request.method == 'POST':

		product.delete()

		if product:

			messages.success(request, 'Product Successfully Deleted!')
			return redirect('store:products')
		else:

			messages.error(request, 'Unable to Update Product!')

		return redirect('store:products')


	context = {'obj':product}
	return render(request, 'store/delete.html',context)

def all_order(request):
	complete = True
	pend = False

	pending = request.GET.get('pending') if request.GET.get('pending') != None else ' '
	if request.GET.get('pending_orders') and pending != None:
		pending_orders = models.Order.objects.filter(is_ordered=pending)
	else:
		pending_orders = models.Order.objects.filter(is_ordered=False)

	products=None
	# orders=None

	completed = request.GET.get('completed') if request.GET.get('completed') != None else ' '
	pending = request.GET.get('pending') if request.GET.get('pending') != None else ' '
	if request.GET.get('completed'):
		orders = models.Order.objects.prefetch_related('items').filter(Q(is_ordered=completed))

	elif request.GET.get('pending'):
		orders = models.Order.objects.prefetch_related('items').filter(Q(is_ordered=pending))

	else:
		orders=models.Order.objects.prefetch_related('items').all()

	order_product = request.GET.get('order_product')
	if request.method == 'GET' and order_product != None :
		order = request.GET.get('order_product') if request.GET.get('order_product') != None else ' '
		products = models.OrderItem.objects.select_related('collection','product')\
											.filter(pk=order)\
											.annotate(total_price=F('price')*F('quantity'))

	context={
			'orders':orders,
			'products':products,
			'order_product':order_product,
			'complete':complete,
			'pend':pend,
			}
	return render(request, 'store/allorders.html',context)
	


def add_product_to_order(request):


	form = forms.OrderItemForm()

	# Choosen Product
	order_id=request.session.get('order_id')
	products = models.OrderItem.objects.filter(order_id=order_id).annotate(total_price=F('price')*F('quantity'))

	total_price = products.aggregate(overall_price=Sum(F('total_price'))) 


	try:
		request.session['total_price'] = str(total_price['overall_price'])
	except:
		pass


	if request.method == 'POST':

		# Get request
		collection_id = request.POST.get('collection')
		collection = models.Collection.objects.get(id=collection_id)
		quantity = request.POST.get('quantity')
		product_id= request.POST.get('product')
		product = models.Product.objects.get(pk=product_id)
		price = request.POST.get('price')

		order,created = models.Order.objects.get_or_create(order_id=order_id)

		request.session['order_id'] = order.order_id


		if product.quantity == 0:
			product_message = format_html('<b>{}</b> is all sold out!',f'{product.name} ')
			messages.warning(request, product_message )

		elif models.OrderItem.objects.filter(product=product,order=order).exists():
			order = models.OrderItem.objects.get(product=product)

			order.quantity +=int(quantity)

			product.quantity -= int(quantity)
			product.save()

			order.save()
			return HttpResponseRedirect('.')
			
		else:

			order_items = models.OrderItem.objects.create(
			collection=collection,
			product = product,
			quantity= quantity,
			price = price,
			order = order
			)
			product.quantity -= int(quantity)
			product.save()

			order_items.save()
			messages.success(request, 'Product Added Successfully !')
			
			return HttpResponseRedirect('.')

			
	context= {'form':form,'products':products,'total_price':total_price,'order_id':order_id}

	return render(request, 'store/order.html',context)


def update_order_product(request,pk):

	verify = 'update'
	order_product = models.OrderItem.objects.get(pk=pk)
	form = forms.OrderItemForm(instance=order_product)

	if request.method == 'POST':

		collection_id = request.POST.get('collection')
		collection = models.Collection.objects.get(id=collection_id)
		quantity = request.POST.get('quantity')
		product_id= request.POST.get('product')
		product = models.Product.objects.get(pk=product_id)
		price = request.POST.get('price')


		if order_product:

			if product.quantity == 0:
				product_message = format_html('<b>{}</b> is all sold out!',f'{product.name} ')
				messages.warning(request, product_message )
			else:
				order_product.collection = collection
				order_product.product = product
				order_product.price = price

				# Get how many quantity increased or reduced
				if order_product.quantity > int(quantity):
					new_quantity = int(order_product.quantity) - int(quantity)
					product.quantity += new_quantity

				elif order_product.quantity < int(quantity):
					new_quantity = int(quantity) - int(order_product.quantity)
					product.quantity -= new_quantity 

				order_product.quantity = int(quantity)

				product.save()

				order_product.save()
				messages.success(request, 'Order Product Successfully Updated!')
				return redirect('store:orders')
		else:
			messages.error(request, 'There is an error while updating the product!')


	context = {'form':form,'verify':verify}

	return render(request, 'store/order.html',context)

def cancel_order(request):

	# Get Order Id From Session
	order_id= request.session.get('order_id')

	order = models.Order.objects.get(order_id=order_id)
	# Get Order Items
	order_items = models.OrderItem.objects.filter(order=order)

	if request.method == 'POST':
		order_items.delete()
		order.delete()
		del request.session['order_id']
		return redirect('store:add_product_to_order')

	context={'obj':order.pk}
	return render(request, 'store/delete.html',context)


def delete_order(request,pk):

	# Delete an Order

	# Get Order
	order = models.Order.objects.get(pk=pk)

	# Get OrderItems
	order_items = models.OrderItem.objects.filter(order=order)

	if request.method == 'POST':
		order_items.delete()
		order.delete()
		return redirect('store:orders')

	context={'obj':order.pk}
	return render(request, 'store/delete.html',context)


def ordered(request):

	# Choosen Product
	order_id=request.session.get('order_id')
	ordered = models.Order.objects.get(order_id=order_id)

	# Get Total Price
	total_price = request.session.get('total_price')

	if ordered:

		order =  models.Order.objects.get(order_id=order_id)

		order.total_price = int(total_price)
		order.is_ordered = True
		items = order.orderitems.all()
		for item in items:
			order.items.add(item)
		order.save()

		messages.success(request, 'Product Ordered Successfully!')

		# Destroy Session
		try : 
			del request.session['order_id']
			del request.session['total_price']
		except:
			pass
	else:
		messages.error(
			request, 'No products exists!')

	context = {'ordered':ordered}
	return render(request, 'store/ordered.html',context)

def edit_staff_account(request):


	staff,created = models.Staff.objects.get_or_create(user=request.user)
	staff_form = forms.StaffForm(instance=staff)
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		gender = request.POST.get('gender')
		user_type = request.POST.get('user_type')
		phone_number = request.POST.get('phone_number')
		shop_name = request.POST.get('shop_name')

		# Update Staff Model
		staff.user_type = user_type
		staff.gender = gender
		staff.phone_number = phone_number
		staff.shop_name = shop_name

		# Update User Model
		user = User.objects.get(pk=request.user.id)
		user.first_name = first_name
		user.last_name = last_name
		user.username = username
		user.email = email

		staff.save()
		user.save()

		messages.success(request, 'Staff Account Updated!')
		return redirect('store:edit_staff_account')

	context = {'staff':staff,'staff_form':staff_form}

	return render(request, 'store/edit_account.html',context)


def load_product(request):

	collection_id = request.GET.get('collection_id')
	products = models.Product.objects.filter(collection_id=collection_id)

	return render(request, 'store/product_load.html',{'products':products})

	# return JsonResponse(list(products.values('product_id','name')), safe=False)

def load_price(request):

	product_id = request.GET.get('product_id')
	product_price = models.Product.objects.filter(product_id=product_id).values('price')
	return JsonResponse(list(product_price),safe=False)

def all_order_product(request):

	products = models.OrderProduct.objects.select_related('collection','product').all()

	context={'products':products}

	return render(request, 'store/allorderproduct.html',context)



def generate_receipt(request):

	# Store Order Information
	order = models.Order.objects.get(pk='C008EB')
	class PDF(FPDF):

		def header(self):

			# Logo
			self.image('./static/images/avatar.jpg',10,8,15)
			# Font
			self.set_font('times','B',23)
			self.set_text_color(7,69,38)
			# Padding
			self.cell(20)
			
			# Title
			self.multi_cell(0,10,f'{order.staff.shop_name}',border=False,ln=True, align='C')
			
			self.set_font('helvetica','I',8)
			self.set_text_color(0,0,0)
			self.cell(20)
			self.cell(0,4,'No 17, Baba-Ode Drive, Idedo, Onibuku, Ogun State',border=False,align='C')
			# line break
			self.ln(4)
			self.cell(20)
			self.cell(0,4,'09070553898',border=False,align='C')
			self.dashed_line(5,30,100,30,dash_length=1,space_length=1)
			
			# line break
			self.ln(5)


	pdf = PDF('P','mm',(105 , 125))  # 105 x 125


	# Create Metadata
	pdf.set_title(f'{order.staff.shop_name} Receipt')
	pdf.set_author(f'{order.staff.shop_name}')

	# Set auto page break
	pdf.set_auto_page_break(auto=True,margin=15)

	# Add a page

	pdf.add_page()

	# Store Order Information
	order = models.Order.objects.get(pk='C008EB')

	# Date Ordered
	pdf.set_font('helvetica','B',9)
	pdf.cell(22,10,'Date Ordered:',ln=False)
	pdf.set_font('helvetica','',9)
	pdf.cell(25,10,f'{order.at_ordered}',ln=False)

	# Padding
	pdf.cell(10)
	
	# Order ID
	pdf.set_font('helvetica','B',9)
	pdf.cell(15,10,'Order ID:',ln=False)
	pdf.set_font('helvetica','',9)
	pdf.set_text_color(7,69,38)
	pdf.cell(25,10,f'#{order.order_id}',ln=True)

	

	pdf.multi_cell(40,10,'Product Name/Desc',border=False,ln=3)

	# vertical line
	pdf.line(50,40,50,90)

	pdf.multi_cell(10,10,'Qty',border=False,ln=3)

	# vertical line
	pdf.line(60,40,60,90)

	pdf.multi_cell(20,10,'Price',border=False,ln=3)

	# vertical line
	pdf.line(80,40,80,90)

	pdf.multi_cell(30,10,'ExtPrice',border=False,ln=True)

	# Horizontal Line
	pdf.line(5,48,100,48)

	# Product
	items= order.items.all()
	for item in items:
		pdf.multi_cell(40,10,f'{item.product.name},({item.product.description})',border=False,ln=3,max_line_height=4)
		pdf.multi_cell(10,10,f'{item.quantity}',border=False,ln=3,max_line_height=4)
		pdf.multi_cell(20,10,f'N{item.price}',border=False,ln=3,max_line_height=4)
		total_price = item.price * item.quantity
		pdf.multi_cell(30,10,f'N{total_price}',border=False,ln=True,max_line_height=4)
	
	# Horizontal Line
	pdf.line(5,90,100,90)

	# Line Space
	pdf.ln(10)

	# Padding
	pdf.cell(50)
	
	pdf.set_font('helvetica','B')
	pdf.multi_cell(20,10,f'Total Price:',border=False,ln=3,max_line_height=2)
	pdf.multi_cell(30,10,f'N{order.total_price}',border=False,ln=True,max_line_height=2)

	# Horizontal Line
	pdf.line(5,97,100,97)
	pdf.cell(0,10,'Thanks for shopping with us!',align='C',ln=True)
	pdf.code39(f"*{order.order_id}*", x=20, y=107,w=1.5,h=10)
	# pdf.cell(0,5,f'{order.order_id}',align='C')
	# pdf.ln(5)
	

	






	# pdf.output(f'{order.order_id}.pdf','F')
	return HttpResponse(bytes(pdf.output()), content_type="application/pdf")
	# return FileResponse(open(f'receipt.pdf','rb'), as_attachment=False, content_type='application/pdf')
	






