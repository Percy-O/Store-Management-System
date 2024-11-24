from django.urls import path
from . import views

from rest_framework_nested import routers


############## API URL  ######################

router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet)
router.register('products', views.ProductViewSet)
router.register('orders', views.OrderViewSet)
router.register('items-1', views.OrderItemViewSet)
router.register('staff', views.StaffViewSet)


orders_router = routers.NestedDefaultRouter(router, 'orders',lookup='order')
orders_router.register('items', views.GetOrderItemViewSet,basename='order-items')


urlpatterns = router.urls + orders_router.urls


# urlpatterns=[

# ]





