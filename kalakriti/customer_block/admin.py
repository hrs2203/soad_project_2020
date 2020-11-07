from django.contrib import admin

from customer_block.models import CustomerModel, BusinessModel

# Register your models here.
admin.site.register(CustomerModel)
admin.site.register(BusinessModel)
