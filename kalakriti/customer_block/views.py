from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, AnonymousUser
from customer_block.forms import (
    user_login_form,
    business_login_form,
    user_signup_form,
    business_signup_form,
)
from customer_block.models import CustomerModel, BusinessModel, OrderModel

from image_model.models import Product
from image_model.forms import upload_product_form

def home_page(request):
    return render(request=request, template_name="homepage.html", context={})


def login_user_page(request):
    context = dict()

    if request.method == "POST":
        form = user_login_form(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=request.POST["userName"],
                password=request.POST["password"],
            )
            if user:
                login(request, user)

    else:
        form = user_login_form()

    context["user"] = request.user
    context["form"] = form
    if request.user.is_authenticated:
        return redirect("/user")

    return render(request=request, template_name="login_user.html", context=context)


def login_business_page(request):
    context = dict()

    if request.method == "POST":
        form = business_login_form(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=request.POST["userName"],
                password=request.POST["password"],
            )
            if user:
                login(request, user)

    else:
        form = business_login_form()

    context["user"] = request.user
    context["form"] = form
    if request.user.is_authenticated:
        return redirect("/business")

    return render(request=request, template_name="login_business.html", context=context)


def logout_page(request):
    logout(request)
    return redirect("/")


def signup_user_page(request):
    context = {}
    form = user_signup_form()
    context["form"] = form
    return render(request=request, template_name="signup_user.html", context=context)


def signup_business_page(request):
    context = {}
    form = business_signup_form()
    context["form"] = form
    return render(
        request=request, template_name="signup_business.html", context=context
    )


def user_page(request):
    return render(request=request, template_name="user_page.html", context={})


def business_page(request):
    return render(request=request, template_name="business_page.html", context={})


def choice_page(request):
    return render(request=request, template_name="design_list_page.html", context={})


def payment_page(request):
    return render(request=request, template_name="make_payment.html", context={})

def upload_custom_product(request):
    context = {}
    form = upload_product_form()
    context["form"] = form
    return render(request=request, template_name="upload_product.html", context=context)