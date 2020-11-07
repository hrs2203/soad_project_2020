from django import forms

class user_login_form(forms.Form):
    userName = forms.CharField(label="user name", max_length=20)
    password = forms.CharField(
        label="password", max_length=20, widget=forms.PasswordInput()
    )


class business_login_form(forms.Form):
    userName = forms.CharField(label="user name", max_length=20)
    password = forms.CharField(
        label="password", max_length=20, widget=forms.PasswordInput()
    )

