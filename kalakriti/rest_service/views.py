from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from customer_block.models import CustomerModel, BusinessModel, OrderModel
from image_model.models import Product

from image_model.views import generateGANImage

from rest_service.serializers import (
    ProductSerializer,
    CustomerModelSerializer,
    BusinessModelSerializer,
    OrderModelSerializer,
)

# Create your views here.
def sampleResponse(request):
    return JsonResponse(
        {
            "api_list": [
                "api/allProduct",
                "api/allCustomer",
                "api/allBusiness",
                "api/allOrder",
                "api/generate_new_image"
            ]
        }
    )


def getGeneratedImage(request):
    """REST api to generate image"""
    newImageUrl = generateGANImage()
    return JsonResponse({"image_url": newImageUrl})


@csrf_exempt
def productList(request):
    """
    List All Product list
    """

    if request.method == "GET":
        allProd = Product.objects.all()
        serializedProd = ProductSerializer(allProd, many=True)
        return JsonResponse(serializedProd.data, safe=False)


@csrf_exempt
def customerList(request):
    """
    List All customer list
    """

    if request.method == "GET":
        allSerializedCustomer = CustomerModel.objects.all()
        serializedCustomerModel = CustomerModelSerializer(
            allSerializedCustomer, many=True
        )
        return JsonResponse(serializedCustomerModel.data, safe=False)


@csrf_exempt
def businessList(request):
    """
    List All business list
    """

    if request.method == "GET":
        allSerializedBusiness = BusinessModel.objects.all()
        serializedBusinessModel = BusinessModelSerializer(
            allSerializedBusiness, many=True
        )
        return JsonResponse(serializedBusinessModel.data, safe=False)


@csrf_exempt
def orderList(request):
    """
    List All order list
    """

    if request.method == "GET":
        allSerializedOrder = OrderModel.objects.all()
        serializedOrderModel = OrderModelSerializer(allSerializedOrder, many=True)
        return JsonResponse(serializedOrderModel.data, safe=False)
