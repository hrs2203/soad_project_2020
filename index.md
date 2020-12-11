# API For Businesses to use

## generate_new_image
<table>
    <tr>
        <td>URL</td>
        <td>{{url}}/api/generate_new_image</td>
    </tr>
    <tr>
        <td>METHOD</td>
        <td>POST</td>
    </tr>
</table>

REQUEST BODY:
```json
{
    "businessId": 7,
    "businessPassword" : "pwd123"
}
```
RESPONSE BODY:
```json
{
    "image_url": "/static/hkusdnauckvmtzmihsql.jpg",
    "message": "$10 has be credited from your account."
}
```

## place_order
<table>
    <tr>
        <td>URL</td>
        <td>{{url}}/api/place_order</td>
    </tr>
    <tr>
        <td>METHOD</td>
        <td>POST</td>
    </tr>
</table> 

REQUEST BODY:
```json
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
RESPONSE BODY:
```json
{
    "orderStatus": [
        {
            "paymentStatus": true,
            "deliveryStatus": false,
            "totalAmount": 40,
            "businessId": 6,
            "productId": 6,
            "customerId": 4,
            "orderId": 2,
            "message": "Order Not placed, Insufficient Balance"
        },
        {
            "paymentStatus": true,
            "deliveryStatus": false,
            "totalAmount": 30,
            "businessId": 5,
            "productId": 7,
            "customerId": 4,
            "orderId": 2,
            "message": "Order Not placed, Insufficient Balance"
        }
    ]
}
```

## confirm_order
<table>
    <tr>
        <td>URL</td>
        <td>{{url}}/api/confirm_order</td>
    </tr>
    <tr>
        <td>METHOD</td>
        <td>POST</td>
    </tr>
</table> 

REQUEST BODY:
```json
{
    "orderId": 12,
    "businessId": 5,
    "businessPassword" : "pwd123"
}
```
RESPONSE BODY:
```json
{
    "orderId": 12,
    "status": true,
    "message": "success"
}
```

## customer_detail
<table>
    <tr>
        <td>URL</td>
        <td>{{url}}/api/customer_detail</td>
    </tr>
    <tr>
        <td>METHOD</td>
        <td>POST</td>
    </tr>
</table>

REQUEST BODY:
```json
{
    "customerId" : 4,
    "password": "pwd123"
}
```
RESPONSE BODY:
```json
{
    "detail": {
        "id": 4,
        "balance": 999190,
        "userModel": 9
    }
}
```

## business_detail
<table>
    <tr>
        <td>URL</td>
        <td> {{url}}/api/business_detail</td>
    </tr>
    <tr>
        <td>METHOD</td>
        <td>POST</td>
    </tr>
</table>

REQUEST BODY:
```json
{
    "businessId" : 7,
    "password": "pwd123"
}
```
RESPONSE BODY:
```json
{
    "detail": {
        "id": 7,
        "balance": 1040,
        "serviceCharge": 50,
        "businessDescription": "some",
        "userModel": 12
    }
}
```

## business_stats
<table>
    <tr>
        <td>URL</td>
        <td>{{url}}/api/business_stats</td>
    </tr>
    <tr>
        <td>METHOD</td>
        <td>POST</td>
    </tr>
</table>

REQUEST BODY:
```json
{
    "businessId" : 7,
    "password": "pwd123"
}
```
RESPONSE BODY:
```json
{
    "businessDetail": {
        "id": 7,
        "balance": 1040,
        "serviceCharge": 50,
        "businessDescription": "some",
        "userModel": 12
    },
    "totalSalesCount": 15,
    "businessSalesCount": 1,
    "businessSales": [
        {
            "id": 5,
            "paymentStatus": true,
            "deliveryStatus": false,
            "totalAmount": 70,
            "productModelLink": 6,
            "userModelLink": 4,
            "businessModelLink": 7
        }
    ]
}
```