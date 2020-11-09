from django.contrib import admin

from customer_block.models import CustomerModel, BusinessModel, OrderModel

# Register your models here.
admin.site.register(CustomerModel)
admin.site.register(BusinessModel)
admin.site.register(OrderModel)
