from django.contrib import admin

from store import models

# Register your models here.
@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
	pass


admin.site.register(models.Collection)
admin.site.register(models.Product)
admin.site.register(models.OrderProduct)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)