from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from image_model.models import Product

DEFAULT_DESCRIPTION = "Business Default Description"


class CustomerModel(models.Model):
    """ Customer model """

    userModel = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = models.IntegerField(default=1000)


class BusinessModel(models.Model):
    """ Business model """

    userModel = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = models.IntegerField(default=1000)
    serviceCharge = models.IntegerField(default=50)
    businessDescription = models.TextField(default=DEFAULT_DESCRIPTION)


class OrderModel(models.Model):
    """ Order model """

    productModelLink = models.OneToOneField(Product, on_delete=models.DO_NOTHING)
    userModelLink = models.OneToOneField(CustomerModel, on_delete=models.DO_NOTHING)
    businessModelLink = models.OneToOneField(BusinessModel, on_delete=models.DO_NOTHING)
    paymentStatus = models.BooleanField(default=False)
    deliveryStatus = models.BooleanField(default=False)
    totalAmount = models.IntegerField(default=0)

