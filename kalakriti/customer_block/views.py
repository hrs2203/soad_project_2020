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
import os, random, string
from pathlib import Path
from image_model.models import Product
from image_model.forms import upload_product_form
from django.core.files.storage import default_storage


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
    print("INNNN")

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

    if request.method == "POST":
        form = user_signup_form(request.POST)
        if form.is_valid():

            try:
                newUser = User.objects.create_user(
                    email=form.cleaned_data["userEmail"],
                    username=form.cleaned_data["userName"],
                    password=form.cleaned_data["password"],
                )
                newUser.is_staff = False
                newUser.save()
            except:
                return redirect("/signup/user")

            newUserDetail = CustomerModel(userModel=newUser)
            newUserDetail.save()
            user = authenticate(
                request,
                username=request.POST["userName"],
                password=request.POST["password"],
            )
            if user:
                login(request, user)
                return redirect("/")
            else:
                print("not auth")

    else:
        form = user_signup_form()

    context["form"] = form

    return render(request=request, template_name="signup_user.html", context=context)


def signup_business_page(request):
    context = {}

    if request.method == "POST":
        form = business_signup_form(request.POST)
        if form.is_valid():

            try:
                newUser = User.objects.create_user(
                    email=form.cleaned_data["businessEmail"],
                    username=form.cleaned_data["businessName"],
                    password=form.cleaned_data["password"],
                )
                newUser.is_staff = True
                newUser.save()
            except:
                print("some error")
                return redirect("/signup/business")

            newBusinessDetail = BusinessModel(
                userModel=newUser,
                serviceCharge=form.cleaned_data["serviceCharge"],
                businessDescription=form.cleaned_data["businessDescription"],
            )
            newBusinessDetail.save()
            user = authenticate(
                request,
                username=request.POST["businessName"],
                password=request.POST["password"],
            )
            if user:
                login(request, user)
                return redirect("/")
            else:
                print("not auth")

    else:
        form = business_signup_form()

    context["form"] = form

    return render(
        request=request, template_name="signup_business.html", context=context
    )


def user_page(request):
    context = dict()
    try:
        context["customerDetail"] = CustomerModel.objects.filter(
            userModel=request.user
        )[0]
    except:
        pass
    return render(request=request, template_name="user_page.html", context=context)


def business_page(request):
    context = dict()
    try:
        context["businessDetail"] = BusinessModel.objects.filter(
            userModel=request.user
        )[0]
    except:
        pass
    return render(request=request, template_name="business_page.html", context=context)


def choice_page(request):
    context = dict()

    context["productList"] = Product.objects.all()[::-1]
    context["dealerList"] = BusinessModel.objects.all()

    return render(
        request=request, template_name="design_list_page.html", context=context
    )


def payment_page(request):
    return render(request=request, template_name="make_payment.html", context={})


def genRandomName(fileName):
    """Generate unique Name for images

    Args:
        fileName (str): fileName to get its extention

    Returns:
        str: unique file name
    """
    fileExt = fileName.split(".")[-1]
    randName = "".join([random.choice(string.ascii_lowercase) for i in range(20)])
    resp = f"{randName}.{fileExt}"

    BASE_FILE = Path(__file__).resolve().parent.parent
    FILE_PATH = os.path.join(BASE_FILE, "image_model", "images", resp)

    while os.path.isfile(FILE_PATH):
        randName = "".join([random.choice(string.ascii_lowercase) for i in range(20)])
        resp = f"{randName}.{fileExt}"

        BASE_FILE = Path(__file__).resolve().parent.parent
        FILE_PATH = os.path.join(BASE_FILE, "image_model", "images", resp)

    return resp


def upload_custom_product(request):

    if not request.user.is_authenticated:
        return redirect("/login/business")

    if not request.user.is_staff:
        return redirect("/user")

    context = {}

    if request.method == "POST":
        form = upload_product_form(request.POST, request.FILES)
        if form.is_valid:

            temp_file = request.FILES["ProductImage"]
            tempFileName = genRandomName(temp_file.name)
            file_name = default_storage.save(tempFileName, temp_file)

            tempProduct = Product(
                ProductName=request.POST["ProductName"],
                ProductUrl=f"/static/{tempFileName}",
                ProductDescription=request.POST["ProductDescription"],
                ProductPrice=request.POST["ProductPrice"],
            )
            tempProduct.save()

        return redirect("/make_choice")

    form = upload_product_form()
    context["form"] = form
    return render(request=request, template_name="upload_product.html", context=context)
