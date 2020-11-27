from rest_framework import serializers

from customer_block.models import CustomerModel, BusinessModel, OrderModel
from image_model.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["ProductName", "ProductUrl", "ProductDescription", "ProductPrice"]
