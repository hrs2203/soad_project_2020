from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

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
                "api/generate_new_image",
            ]
        }
    )


def getGeneratedImage(request):
    """REST api to generate image"""
    newImageUrl = generateGANImage()
    return JsonResponse({"image_url": newImageUrl})


@csrf_exempt
def confirmOrderDelivery(request):
    """
    Confirm payment from business side.

    - request body
    ```
    {
        "orderId": 5,
        "businessId": 4,
        "businessPassword" : "pwd123"
    }
    ```

    - response body
    ```
    {
        "orderId": 5,
        "status" : true | false
    }
    ```
    """
    if request.method == "POST":
        reqData = json.loads(request.body)

        orderId = reqData["orderId"]
        businessId = reqData["businessId"]
        businessPassword = reqData["businessPassword"]

        ## ====== confirm credentials ======

        businessObjList = BusinessModel.objects.filter(id=businessId)
        if len(businessObjList) == 0:
            return JsonResponse({"message": "Invalid business Id"})

        businessObj = businessObjList[0]
        if not businessObj.userModel.check_password(businessPassword):
            return JsonResponse({"message": "Invalid business credentials"})

        ## ==============================

        try:
            tempOrderObj = OrderModel.objects.filter(id=orderId)[0]

            if not (tempOrderObj.businessModelLink == businessObj):
                return JsonResponse({"message": "Invalid business credentials"})

            tempOrderObj.deliveryStatus = True
            tempOrderObj.save()
            return JsonResponse(
                {
                    "orderId": orderId,
                    "status": tempOrderObj.deliveryStatus,
                    "message": "success",
                }
            )
        except:
            return JsonResponse(
                {"orderId": orderId, "status": False, "message": "Invalid Order Id"}
            )


@csrf_exempt
def placeOrder(request):
    """ Place Bulk Order 

    - Place Order as list of json
    - Product Order Sample
    ```
    {
        "orderList" : [
            {
                "businessId" : 6,
                "productId" : 6,
                "customerId" : 4
            },
            {
                "businessId" : 5,
                "productId" : 7,
                "customerId" : 4
            }
        ]
    }
    ```
    
    - Response Format

    ```
    {
        "orderStatus": [
            {
                "paymentStatus": false,
                "deliveryStatus": false,
                "totalAmount": 0,
                "businessId": 6,
                "productId": 6,
                "customerId": 4,
                "orderId": 2,
                "message": "Order Not placed, Insufficient Balance"
            },
            {
                "paymentStatus": false,
                "deliveryStatus": false,
                "totalAmount": 0,
                "businessId": 5,
                "productId": 7,
                "customerId": 4,
                "orderId": 2,
                "message": "Order Not placed, Insufficient Balance"
            }
        ]
    }
    ```
    """

    responseList = []

    if request.method == "POST":

        requestList = list()

        try:
            requestList = json.loads(request.body)["orderList"]
        except:
            requestList = list()

        for order in requestList:
            tempResponse = dict()

            tempResponse["paymentStatus"] = False
            tempResponse["deliveryStatus"] = False
            tempResponse["totalAmount"] = 0
            tempResponse["businessId"] = order["businessId"]
            tempResponse["productId"] = order["productId"]
            tempResponse["customerId"] = order["customerId"]
            tempResponse["orderId"] = 2
            tempResponse["message"] = "Order Not placed, Insufficient Balance"

            ## ======= make order =======

            context = dict()

            context["businessId"] = None
            context["productId"] = None
            context["businessObject"] = None
            context["productObject"] = None
            context["customerDetail"] = None
            context["canUserPay"] = False
            context["totalPaymentAmount"] = 0

            try:
                context["businessId"] = order["businessId"]
                context["productId"] = order["productId"]
                context["businessObject"] = BusinessModel.objects.filter(
                    id=context["businessId"]
                )[0]
                context["productObject"] = Product.objects.filter(
                    id=context["productId"]
                )[0]
                context["totalPaymentAmount"] = (
                    context["businessObject"].serviceCharge
                    + context["productObject"].ProductPrice
                )
                context["customerDetail"] = CustomerModel.objects.get(
                    id=order["customerId"]
                )
                context["canUserPay"] = (
                    context["customerDetail"].balance >= context["totalPaymentAmount"]
                )
                tempResponse["paymentStatus"] = context["canUserPay"]
                tempResponse["totalAmount"] = context["totalPaymentAmount"]

                if tempResponse["paymentStatus"]:
                    tempCustomerModel = CustomerModel.objects.get(
                        id=order["customerId"]
                    )
                    tempCustomerModel.balance -= tempResponse["totalAmount"]
                    tempCustomerModel.save()

                    tempBusinessModel = BusinessModel.objects.get(
                        id=order["businessId"]
                    )
                    tempBusinessModel.balance += tempResponse["totalAmount"]
                    tempBusinessModel.save()

                    tempProductModel = Product.objects.get(id=order["productId"])

                    tempOrder = OrderModel(
                        productModelLink=tempProductModel,
                        userModelLink=tempCustomerModel,
                        businessModelLink=tempBusinessModel,
                        paymentStatus=True,
                        deliveryStatus=False,
                        totalAmount=tempResponse["totalAmount"],
                    )
                    tempOrder.save()

            except:
                tempResponse["paymentStatus"] = False
                tempResponse["deliveryStatus"] = False
                tempResponse["totalAmount"] = 0
                tempResponse["businessId"] = order["businessId"]
                tempResponse["productId"] = order["productId"]
                tempResponse["customerId"] = order["customerId"]
                tempResponse["orderId"] = 2
                tempResponse["message"] = "Order Not placed, Insufficient Balance"

            ## ==========================

            responseList.append(tempResponse)

    return JsonResponse({"orderStatus": responseList})


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
