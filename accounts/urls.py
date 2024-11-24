from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
	path('login',views.staff_login,name='login'),
	path('logout',views.staff_logout,name='logout'),
	path('register',views.staff_register,name='register'),
	# path('edit/staff',views.edit_staff_account,name='edit_staff_account'),
]