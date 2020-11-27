from rest_framework import serializers

from customer_block.models import CustomerModel, BusinessModel, OrderModel
from image_model.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Default Serializer from Product Class
    """
    class Meta:
        model = Product
        fields = '__all__'

class CustomerModelSerializer(serializers.ModelSerializer):
    """
    Default Serializer from CustomerModel Class
    """
    class Meta:
        model = CustomerModel
        fields = '__all__'

class BusinessModelSerializer(serializers.ModelSerializer):
    """
    Default Serializer from BusinessModel Class
    """
    class Meta:
        model = BusinessModel
        fields = '__all__'

class OrderModelSerializer(serializers.ModelSerializer):
    """
    Default Serializer from OrderModel Class
    """
    class Meta:
        model = OrderModel
        fields = '__all__'
