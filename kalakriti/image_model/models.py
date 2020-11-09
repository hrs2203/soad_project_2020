from django.db import models

# Create your models here.

DEFAULT_DESCRIPTION = "Product Default Description"

class Product(models.Model):
    """ Product model """
    ProductName = models.CharField(max_length=20)
    ProductUrl = models.CharField(max_length=50)
    ProductDescription = models.CharField(max_length=50, default=DEFAULT_DESCRIPTION)
    ProductPrice = models.IntegerField(default=30)
