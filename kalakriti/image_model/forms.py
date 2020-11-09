from django import forms


class upload_product_form(forms.Form):
    ProductName = forms.CharField(
        label="product name",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ProductDescription = forms.CharField(
        label="product description",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ProductPrice = forms.IntegerField(
        label="product price", widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    ProductImage = forms.ImageField(
        label="upload product Image",
        widget=forms.FileInput(attrs={"class": "form-control-file"}),
    )

