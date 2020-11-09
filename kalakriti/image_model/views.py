from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def sampleResponse(request):
    return JsonResponse({"model": "sample response"})

# TODO: Make this happen
def uploadProduct(request):
    return JsonResponse({"model": "sample response"})