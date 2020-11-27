from django.urls import path
from rest_service import views

urlpatterns = [
    path('', views.sampleResponse),
    path('allProduct', views.productList )
]
