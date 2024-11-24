from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response

from store import models
from .serializers import CollectionSerializer,ProductSerializer,UpdateOrderSerializer,OrderSerializer,OrderItemSerializer,CreateOrderItemSerializer,CreateOrderItemSerializer1,StaffSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadonly


###############  SERIALIZER CLASS   #########################


class CollectionViewSet(ModelViewSet):

	serializer_class = CollectionSerializer
	queryset = models.Collection.objects.all()
	permission_classes = [IsAdminOrReadonly]
	filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
	filterset_fields = ['title']
	# Overide Pagination Class
	pagination_class = DefaultPagination
	search_fields = ['title']
	ordering_fields = ['title']


	def destroy(self,request,*args,**kwargs):
		if models.Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
			return Response(
				{'error':'Collection cannot be deleted because it includes one or more products. '}, 
				status=status.HTTP_405_METHOD_NOT_ALLOWED)
		return super().destroy(request,*args,**kwargs)


class ProductViewSet(ModelViewSet):

	serializer_class = ProductSerializer
	queryset = models.Product.objects.select_related('collection').all()
	filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
	filterset_fields = ['collection_id']
	# Overiding Filter Class
	filterset_class =  ProductFilter
	# Overide Pagination Class
	pagination_class = DefaultPagination
	search_fields = ['name','product_id']
	ordering_fields = ['price']


	def destroy(self,request,*args,**kwargs):
		if models.OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
			return Response(
				{'error':'Product cannot be deleted because it is associated with an order item'},
				status=status.HTTP_405_METHOD_NOT_ALLOWED)

		return super().destroy(request,*args,**kwargs)


class OrderViewSet(ModelViewSet):

	http_method_names = ['get','post','patch','delete']
	serializer_class = OrderSerializer
	queryset = models.Order.objects.all()

	def get_permissions(self):
		if self.request.method in ['PATCH','DELETE']:
			return [IsAdminUser()]
		else:
			return [IsAuthenticated()]
			
	def get_serializer_class(self):

		if self.request.method in ['POST','GET']:
			return OrderSerializer
		return UpdateOrderSerializer

	def get_serializer_context(self):
		return {'user_id':self.request.user.id}

class GetOrderItemViewSet(ModelViewSet):

	http_method_names = ['get','post','delete']
	
	def get_queryset(self):
		queryset = models.OrderItem.objects.select_related('collection','product').filter(order_id=self.kwargs['order_pk'])
		return queryset

	def get_serializer_class(self):

		if self.request.method == 'POST':
			return CreateOrderItemSerializer
		else:
			return OrderItemSerializer

	def get_serializer_context(self):
		return {'order_id':self.kwargs['order_pk'],'data':self.request.data}

class OrderItemViewSet(ModelViewSet):

	# http_method_names = ['get','post','delete']


	queryset = models.OrderItem.objects.select_related('collection','product').all()

	# serializer_class = OrderItemSerailizer

	def get_serializer_class(self):

		if self.request.method == 'POST':
			return CreateOrderItemSerializer1
		return OrderItemSerializer

	def get_serializer_context(self):
		if self.request.method =='POST':
			if self.request.data:
				return{'data':self.request.data}


class StaffViewSet(ModelViewSet):

	queryset = models.Staff.objects.select_related('user').all()
	serializer_class = StaffSerializer

	def get_permissions(self):

		if self.request.method == 'GET':
			return [AllowAny()]
		else:
			return [IsAuthenticated()]


		def get_serializer_context(self):
			return {'user_id':self.request.user.id}

	@action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
	def me(self,request):
		staff = models.Staff.objects.get(user_id=request.user.id)

		if request.method == 'GET':
			serializer = StaffSerializer(staff)
			return Response(serializer.data)
		elif request.method == 'PUT':
			serializer = StaffSerializer(staff,data=request.data)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
				






