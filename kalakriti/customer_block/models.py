from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class CustomerModel(models.Model):
    """ Customer model """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.IntegerField(default=1000)


class BusinessModel(models.Model):
    """ Business model """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.IntegerField(default=1000)