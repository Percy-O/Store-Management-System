from django.urls import path
from store import views


app_name='store'

urlpatterns=[
	path('dashboard/',views.dashboard,name='dashboard'),
	path('collection/',views.add_collection,name='collection'),
	path('collection/<int:pk>/update',views.update_collection,name='update_collection'),
	path('collection/<int:pk>/delete',views.delete_collection,name='delete_collection'),

	path('products/',views.all_product,name='products'),
	path('product/',views.add_product,name='product'),
	path('product/<str:slug>/update',views.update_product,name='update_product'),
	path('product/<str:slug>/delete',views.delete_product,name='delete_product'),

	
	path('order/add/',views.add_product_to_order,name='add_product_to_order'),
	path('order/product/<int:pk>/update',views.update_order_product,name='update_order_product'),
	path('ordered/product/',views.ordered,name='ordered'),
	path('order/all/',views.all_order,name='orders'),
	path('order/cancel/',views.cancel_order,name='cancel_order'),
	path('order/<str:pk>/delete',views.delete_order,name='delete_order'),

	path('load/product',views.load_product,name='load_product'),
	path('load/price',views.load_price,name='load_price'),

	path('print/receipt',views.generate_receipt,name='receipt'),

	path('edit/staff',views.edit_staff_account,name='edit_staff_account'),
	

]


