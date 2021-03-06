from django.urls import path
import customer_block.views as v

urlpatterns = [
    path('', v.home_page, name="home_page"),
    path('logout', v.logout_page, name="logout_page"),
    path('login/user', v.login_user_page, name="login_user_page"),
    path('login/business', v.login_business_page, name="login_business_page"),
    path('signup/user', v.signup_user_page, name="signup_user_page"),
    path('signup/business', v.signup_business_page, name="signup_business_page"),
    path('user', v.user_page, name="user_page"),
    path('business', v.business_page, name="business_page"),
    path('make_choice', v.choice_page, name="choice_page"),
    path('make_payment', v.payment_page, name="payment_page"),
    path('confirm_payment', v.confirm_payment_page, name="confirm_payment_page"),
    path('upload_product', v.upload_custom_product, name="upload_custom_product"),
    path('deliver_product', v.deliver_custom_product, name="deliver_custom_product"),
    
    path('add_more_money', v.add_money_to_user, name="money_page"),
]
