from django.urls import path
import image_model.views as v

urlpatterns = [
    path('', v.sampleResponse),
    path('upload_product', v.uploadProduct, name="upload_product")
]
