from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser

import json

import os, random, string
from pathlib import Path
from django.core.files.storage import default_storage

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


# registerBusiness
# registerCustomer


@csrf_exempt
def registerBusiness(request):
    """Register your business

    - request body
    ```
    {
        "email" : "email",
        "businessName" : "businessName",
        "password" : "password",
        "description" : "description",
        "serviceCharge" : 30
    }
    ```

    - response body
    ```
    {
        "id" : x,
        "email" : "email",
        "businessName" : "businessName",
        "password" : "password",
        "description" : "description",
        "serviceCharge" : 30 
    }
    ```
    """
    if request.method == "POST":
        reqData = json.loads(request.body)

        email = reqData["email"]
        businessName = reqData["businessName"]
        password = reqData["password"]
        description = reqData["description"]
        try:
            serviceCharge = int(reqData["serviceCharge"])
        except:
            serviceCharge = 10

        newUser = User.objects.create_user(
            email=email, username=businessName, password=password,
        )
        newUser.is_staff = True
        newUser.save()

        newBusinessDetail = BusinessModel(
            userModel=newUser,
            serviceCharge=serviceCharge,
            businessDescription=description,
        )
        newBusinessDetail.save()

        tempBusiness = BusinessModelSerializer(newBusinessDetail)

        return JsonResponse(tempBusiness.data)

@csrf_exempt
def registerCustomer(request):
    """ register customer api
    - request body
    ```
    {
        "email" : "email",
        "customerName" : "customerName",
        "password" : "password",
    }
    ```

    - response body
    ```
    {
        "id" : x,
        "email" : "email",
        "customerName" : "customerName",
        "password" : "password", 
    }
    """
    if request.method == 'POST':

        reqData = json.loads(request.body)

        email = reqData["email"]
        customerName = reqData["customerName"]
        password = reqData["password"]

        newUser = User.objects.create_user(
            email=email, username=customerName, password=password,
        )
        newUser.is_staff = False
        newUser.save()

        newUserDetail = CustomerModel(userModel=newUser)
        newUserDetail.save()

        tempCustomer = CustomerModelSerializer(newUserDetail)

        return JsonResponse(tempCustomer.data)


@csrf_exempt
def getGeneratedImage(request):
    """
    - REST api to generate image only for businesses
    - image generation charge $10       
    
    - request body
    ```
    {
        "businessId": 4,
        "businessPassword" : "pwd123"
    }
    ```

    - response body
    ```
    {
        "image_url": "newImageUrl"
    }
    ```
    """
    if request.method == "POST":

        reqData = json.loads(request.body)

        businessId = reqData["businessId"]
        businessPassword = reqData["businessPassword"]

        ## ====== confirm credentials ======

        businessObjList = BusinessModel.objects.filter(id=businessId)
        if len(businessObjList) == 0:
            return JsonResponse({"message": "Invalid business Id"})

        businessObj = businessObjList[0]
        if not businessObj.userModel.check_password(businessPassword):
            return JsonResponse({"message": "Invalid business credentials"})

        if businessObj.balance < 10:
            return JsonResponse({"message": "Insufficient Balance"})

        businessObj.balance -= 10
        businessObj.save()

        newImageUrl = generateGANImage()
        return JsonResponse(
            {
                "image_url": newImageUrl,
                "message": "$10 has be credited from your account.",
            }
        )


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
                    tempResponse["orderId"] = tempOrder.id
                    tempResponse["message"] = "Order placed."

            except:
                tempResponse["paymentStatus"] = False
                tempResponse["deliveryStatus"] = False
                tempResponse["totalAmount"] = 0
                tempResponse["businessId"] = order["businessId"]
                tempResponse["productId"] = order["productId"]
                tempResponse["customerId"] = order["customerId"]
                tempResponse["orderId"] = "None"
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
def customerDetail(request):
    """
    Individual Customer Detail

    - request body
    ```
    {
        "customerId" : 5,
        "password": "pwd123"
    }
    ```

    - response body
    ```
    {
        "detail": <Customer Object>
    }
    ```
    """

    if request.method == "POST":
        reqData = json.loads(request.body)

        customerId = reqData["customerId"]
        password = reqData["password"]

        CustomerObjList = CustomerModel.objects.filter(id=customerId)
        if len(CustomerObjList) == 0:
            return JsonResponse({"message": "Invalid Customer Id"})

        CustomerObj = CustomerObjList[0]
        if not CustomerObj.userModel.check_password(password):
            return JsonResponse({"message": "Invalid Customer credentials"})

        tempCustomer = CustomerModelSerializer(CustomerObj)
        return JsonResponse({"detail": tempCustomer.data})


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
def businessDetail(request):
    """
    Individual Business Detail

    - request body
    ```
    {
        "businessId" : 5,
        "password": "pwd123"
    }
    ```

    - response body
    ```
    {
        "detail": <Business Object>
    }
    ```
    """

    if request.method == "POST":
        reqData = json.loads(request.body)

        businessId = reqData["businessId"]
        password = reqData["password"]

        BusinessObjList = BusinessModel.objects.filter(id=businessId)
        if len(BusinessObjList) == 0:
            return JsonResponse({"message": "Invalid Business Id"})

        BusinessObj = BusinessObjList[0]
        if not BusinessObj.userModel.check_password(password):
            return JsonResponse({"message": "Invalid Business credentials"})

        tempBusiness = BusinessModelSerializer(BusinessObj)
        return JsonResponse({"detail": tempBusiness.data})


@csrf_exempt
def businessStats(request):
    """
    Individual Business Detail

    - request body
    ```
    {
        "businessId" : 5,
        "password": "pwd123"
    }
    ```

    - response body
    ```
    {
        "businessDetail": <Business Object>,
        "businessSales": { ...},
        "totalSales": { ...}
    }
    ```
    """

    if request.method == "POST":
        reqData = json.loads(request.body)

        businessId = reqData["businessId"]
        password = reqData["password"]

        BusinessObjList = BusinessModel.objects.filter(id=businessId)
        if len(BusinessObjList) == 0:
            return JsonResponse({"message": "Invalid Business Id"})

        BusinessObj = BusinessObjList[0]
        if not BusinessObj.userModel.check_password(password):
            return JsonResponse({"message": "Invalid Business credentials"})

        tempBusiness = BusinessModelSerializer(BusinessObj)

        orderCount = OrderModel.objects.all().count()
        businessOrder = OrderModel.objects.filter(businessModelLink=BusinessObj)

        tempbusinessOrder = OrderModelSerializer(businessOrder, many=True)

        return JsonResponse(
            {
                "businessDetail": tempBusiness.data,
                "totalSalesCount": orderCount,
                "businessSalesCount": len(tempbusinessOrder.data),
                "businessSales": tempbusinessOrder.data,
            }
        )


@csrf_exempt
def orderList(request):
    """
    List All order list
    """

    if request.method == "GET":
        allSerializedOrder = OrderModel.objects.all()
        serializedOrderModel = OrderModelSerializer(allSerializedOrder, many=True)
        return JsonResponse(serializedOrderModel.data, safe=False)


def genRandomName(fileName):
    """Generate unique Name for images

    Args:
        fileName (str): fileName to get its extention

    Returns:
        str: unique file name
    """
    fileExt = fileName.split(".")[-1]
    randName = "".join([random.choice(string.ascii_lowercase) for i in range(20)])
    resp = f"{randName}.{fileExt}"

    BASE_FILE = Path(__file__).resolve().parent.parent
    FILE_PATH = os.path.join(BASE_FILE, "image_model", "images", resp)

    while os.path.isfile(FILE_PATH):
        randName = "".join([random.choice(string.ascii_lowercase) for i in range(20)])
        resp = f"{randName}.{fileExt}"

        BASE_FILE = Path(__file__).resolve().parent.parent
        FILE_PATH = os.path.join(BASE_FILE, "image_model", "images", resp)

    return resp


@csrf_exempt
def uploadProduct(request):
    if request.method == "POST":
        # reqData = json.loads(request.body)

        product_name = request.POST["product_name"]
        description = request.POST["description"]
        product_price = request.POST["product_price"]

        temp_file = request.FILES["uploaded_image"]
        tempFileName = genRandomName(temp_file.name)
        file_name = default_storage.save(tempFileName, temp_file)

        tempProduct = Product(
            ProductName=product_name,
            ProductUrl=f"/static/{tempFileName}",
            ProductDescription=description,
            ProductPrice=int(product_price),
        )
        tempProduct.save()

        tempProductDetail = ProductSerializer(tempProduct)

        return JsonResponse(
            {
                "newImageUrl": f"/static/{tempFileName}",
                "productId": tempProduct.id,
                "productDetail": tempProductDetail.data,
            }
        )


@csrf_exempt
def updateBusinessDiscription(request):
    """
    Edit you business description and make it a notice board

    - request body
    ```
    {
        "businessId" : 5,
        "password": "pwd123",
        "description" : "new description"
    }
    ```

    - response body
    ```
    {
        "businessId" : 5,
        "businessDetail": <object>
    }
    ```
    """

    if request.method == "POST":
        reqData = json.loads(request.body)

        businessId = reqData["businessId"]
        password = reqData["password"]
        newDesc = reqData["description"]

        BusinessObjList = BusinessModel.objects.filter(id=businessId)
        if len(BusinessObjList) == 0:
            return JsonResponse({"message": "Invalid Business Id"})

        BusinessObj = BusinessObjList[0]
        if not BusinessObj.userModel.check_password(password):
            return JsonResponse({"message": "Invalid Business credentials"})

        BusinessObj.businessDescription = newDesc
        BusinessObj.save()

        tempBusiness = BusinessModelSerializer(BusinessObj)

        return JsonResponse(
            {"businessId": businessId, "businessDetail": tempBusiness.data}
        )


@csrf_exempt
def addMoneyToUser(request):
    """
    Add Credit to user account from business account

    - request body
    ```
    {
        "businessId" : 5,
        "password": "pwd123",
        "customerId": 4,
        "amount" : 10
    }
    ```

    - response body
    ```
    {
        "businessId" : 5,
        "businessBalance": 1213,
        "customerId" : 4,
        "customerBalance": 1213,
    }
    ```
    """

    if request.method == "POST":
        reqData = json.loads(request.body)

        businessId = reqData["businessId"]
        password = reqData["password"]
        customerId = reqData["customerId"]
        try:
            amount = int(reqData["amount"])
        except:
            amount = 0

        BusinessObjList = BusinessModel.objects.filter(id=businessId)
        if len(BusinessObjList) == 0:
            return JsonResponse({"message": "Invalid Business Id"})

        CustomerObjList = CustomerModel.objects.filter(id=customerId)
        if len(CustomerObjList) == 0:
            return JsonResponse({"message": "Invalid Customer Id"})

        BusinessObj = BusinessObjList[0]
        if not BusinessObj.userModel.check_password(password):
            return JsonResponse({"message": "Invalid Business credentials"})

        CustomerObj = CustomerObjList[0]
        if not CustomerObj.userModel.check_password(password):
            return JsonResponse({"message": "Invalid Customer credentials"})

        BusinessObj.balance -= amount
        BusinessObj.save()

        CustomerObj.balance += amount
        CustomerObj.save()

        return JsonResponse(
            {
                "businessId": BusinessObj.id,
                "businessBalance": BusinessObj.balance,
                "customerId": CustomerObj.id,
                "customerBalance": CustomerObj.balance,
            }
        )

