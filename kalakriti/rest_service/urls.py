from django.urls import path
from rest_service import views

urlpatterns = [
    path('', views.sampleResponse),
    path('allProduct', views.productList, name="all_product_list"),
    path('allCustomer', views.customerList, name="all_customer_list"),
    path('allBusiness', views.businessList, name="all_business_list"),
    path('allOrder', views.orderList, name="all_order_list"),
]
