from django.urls import path
import rest_service.views as v

urlpatterns = [
    path('', v.sampleResponse),
]
