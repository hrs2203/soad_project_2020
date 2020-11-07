from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home_page(request):
    return render(request=request, template_name="homepage.html", context={})


def login_user_page(request):
    return render(request=request, template_name="login_user.html", context={})

def login_business_page(request):
    return render(request=request, template_name="login_business.html", context={})

def signup_user_page(request):
    return render(request=request, template_name="signup_user.html", context={})

def signup_business_page(request):
    return render(request=request, template_name="signup_business.html", context={})

def user_page(request):
    return render(request=request, template_name="user_page.html", context={})

def business_page(request):
    return render(request=request, template_name="business_page.html", context={})

def choice_page(request):
    return render(request=request, template_name="design_list_page.html", context={})

def payment_page(request):
    return render(request=request, template_name="make_payment.html", context={})









