from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from customer_block.models import CustomerModel, BusinessModel, OrderModel
from image_model.models import Product

from rest_service.serializers import ProductSerializer

# Create your views here.
def sampleResponse(request):
    return JsonResponse({"model": "sample api response"})


# @csrf_exempt
def productList(request):
    """
    List All Product
    """

    if request.method == "GET":
        allProd = Product.objects.all()
        serializedProd = ProductSerializer(allProd, many=True)
        return JsonResponse(serializedProd.data, safe=False)
