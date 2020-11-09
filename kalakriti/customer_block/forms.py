from django import forms


class user_login_form(forms.Form):
    userName = forms.CharField(
        label="user name",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="password",
        max_length=20,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class business_login_form(forms.Form):
    userName = forms.CharField(
        label="user name",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="password",
        max_length=20,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class user_signup_form(forms.Form):
    userEmail = forms.EmailField(
        label="email",
        max_length=30,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    userName = forms.CharField(
        label="user name",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="password",
        max_length=20,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    confirm_password = forms.CharField(
        label="confirm password",
        max_length=20,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class business_signup_form(forms.Form):
    businessEmail = forms.EmailField(
        label="email",
        max_length=30,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    businessName = forms.CharField(
        label="business name",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    businessDescription = forms.CharField(
        label="description",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    serviceCharge = forms.IntegerField(label="service charge", widget=forms.NumberInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label="password",
        max_length=20,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    confirm_password = forms.CharField(
        label="confirm password",
        max_length=20,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
