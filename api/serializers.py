from decimal import Decimal
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.conf import settings
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from store.models import Collection,Product,Order,OrderItem,Staff



class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):

        fields = ['id','username','password','email','first_name','last_name']


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):

        fields = ['id','username','email','first_name','last_name']


# class ExcerptUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = settings.AUTH_USER_MODEL
#         fields = ['id','username','email','first_name','last_name']

class StaffSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)
    class Meta:

        model = Staff
        fields= ['id','user_id','phone_number','gender','shop_name']

    def create(self,validated_data):

        user_id = self.context['user_id']
        return Staff.objects.create(user_id=user_id,**validated_data)


class CollectionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Collection
		fields = ['id','title']

class ProductSerializer(serializers.ModelSerializer):

    # collection = CollectionSerializer()
    product_id = serializers.CharField(read_only=True)
    class Meta:
        model = Product
        fields = ['product_id','name','description','slug','price','quantity','collection']

class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['product_id','name','collection','price']



class OrderItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()


    class Meta:
        model = OrderItem
        fields = ['id','collection','product','quantity','price','order','total_price']

    total_price = serializers.SerializerMethodField('price')

    def price(self,item:OrderItem):
        price = item.price * item.quantity 

        return price





class CreateOrderItemSerializer1(serializers.ModelSerializer):

    order_id = serializers.CharField()
    user_id = serializers.CharField()
    price= serializers.DecimalField(max_digits=8,decimal_places=2,read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','collection','product','quantity','order_id','price','user_id']

       
    def save(self,*args,**kwargs):
        data = self.context['data']

        get_product= Product.objects.get(pk=data['product'])
       



        # Update Product Quantity
        get_product.quantity -= int(data['quantity']) 
        
        # Check if order item exists
        if get_product.quantity == 0:
            raise serializers.ValidationError('The Product Choosen Is All Sold Out!')

        elif OrderItem.objects.filter(product_id=data['product'],order_id=data['order_id']).exists():

                # Add to quantity
            # update_order_item_quantity = get_object_or_404(OrderItem,order_id=data['order_id'])
            update_order_item_quantity = OrderItem.objects.get(product_id=data['product'],order_id=data['order_id'])

            update_order_item_quantity.quantity += int(data['quantity']) 
            get_product.quantity -=int(data['quantity']) 
            update_order_item_quantity.save()

        else:


            # Adding the price
            get_price = get_product.price
            if data['order_id'] is not None:
                self.instance = OrderItem.objects.create(price=get_price,**self.validated_data)
            else:
                order_id = self.context['order_id']
                self.instance = OrderItem.objects.create(price=get_price,order_id=order_id,**self.validated_data)

            # Update Order
            order = get_object_or_404(Order,pk=data['order_id'])
            # order = Order.objects.get(pk=data['order_id'])

            items = order.orderitems.all()
            # Using List Comprehension to get the total price
            order.total_price = sum([item.quantity * item.price for item in items])

            # Add All Order Items To Many Many Field 
            for item in items:
                order.items.add(item)

            order.is_ordered = True

            order.save()
            return self.instance
            
            
        get_product.save()

class CreateOrderItemSerializer(serializers.ModelSerializer):

    order_id = serializers.CharField(read_only=True)
     
    price= serializers.DecimalField(max_digits=8,decimal_places=2,read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','collection','product','quantity','order_id','price']

       
    def save(self,*args,**kwargs):
        data = self.context['data']
        order_id = self.context['order_id']

        get_product= Product.objects.get(pk=data['product'])

        # Update Product Quantity
        get_product.quantity -= int(data['quantity']) 
        
        # Check if order item exists
        if get_product.quantity == 0:
            raise serializers.ValidationError('The Product Choosen Is All Sold Out!')

        elif OrderItem.objects.filter(product_id=data['product'],order_id=order_id).exists():

                # Add to quantity
            # update_order_item_quantity = get_object_or_404(OrderItem,order_id=data['order_id'])
            update_order_item_quantity = OrderItem.objects.get(product_id=data['product'],order_id=order_id)

            update_order_item_quantity.quantity += int(data['quantity']) 
            get_product.quantity -=int(data['quantity']) 
            update_order_item_quantity.save()

        else:


            # Adding the price
            get_price = get_product.price
            order_id = self.context['order_id']
            self.instance = OrderItem.objects.create(price=get_price,order_id=order_id,**self.validated_data)

            # Update Order
            order = get_object_or_404(Order,pk=order_id)
            # order = Order.objects.get(pk=data['order_id'])

            items = order.orderitems.all()
            # Using List Comprehension to get the total price
            order.total_price = Decimal(sum([item.quantity * item.price for item in items]))

            # Add All Order Items To Many Many Field 
            for item in items:
                order.items.add(item)

            order.is_ordered = True

            order.save()
            return self.instance
            
            
        get_product.save()

class OrderSerializer(serializers.ModelSerializer):

    order_id = serializers.CharField(read_only=True)
    total_price = serializers.CharField(read_only=True)
    is_ordered = serializers.BooleanField(read_only=True)
    staff = serializers.CharField(read_only=True)
    orderitems = OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['order_id','staff','is_ordered','orderitems','total_price',]

    # def save(self,*args,**kwargs):

    #     Order

    def create(self,validated_data):

        user_id = self.context['user_id']

        staff,created = Staff.objects.get_or_create(user_id=user_id)

        return Order.objects.create(staff=staff,**validated_data)


class UpdateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['is_ordered']






    




    