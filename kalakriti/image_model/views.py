from django.shortcuts import render
from django.http import JsonResponse

import os, random, string
from pathlib import Path

def sampleResponse(request):
    return JsonResponse({"model": "sample response"})

# TODO: REST API
def uploadProduct(request):
    return JsonResponse({"model": "sample response"})

def generateGANImage():
    """ Generate GAN image function """
    generatedImageUrl = f"/static/"

    # file in which we have to look newly generated image
    BASE_FILE = Path(__file__).resolve().parent.parent
    FILE_PATH = os.path.join(BASE_FILE, "image_model", "generated_images")

    # list of all possible file
    imageNameList = os.listdir(FILE_PATH)

    # randomly selected on file
    imageName = imageNameList[ random.randint(0, len(imageNameList)) ]

    # imageAccessUrl
    generatedImageUrl = f"/static/{imageName}"

    return generatedImageUrl