from django.urls import path
from rest_service import views

urlpatterns = [
    path("", views.sampleResponse),
    path("allProduct", views.productList, name="all_productList"),
    path("allCustomer", views.customerList, name="all_customerList"),
    path("allBusiness", views.businessList, name="all_businessList"),
    path("allOrder", views.orderList, name="all_orderList"),
    path("generate_new_image", views.getGeneratedImage, name="generateNewImage"),
    path("place_order", views.placeOrder, name="placeOrder"),
    path("confirm_order", views.confirmOrderDelivery, name="confirmOrder"),
]
