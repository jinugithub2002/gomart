from django import forms
from django.contrib.auth.models import User
from .models import tbl_country,tbl_category,tbl_customer
from .models import tbl_brands,tbl_product
from django.contrib.auth.forms import UserCreationForm
from .models import DeliveryPartner


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class TblCountryForm(forms.ModelForm):
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = tbl_country
        fields = ['country_name', 'status']
        

class BrandForm(forms.ModelForm):
    class Meta:
        model = tbl_brands
        fields = ['logo', 'brand_name', 'status']
        widgets = {
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'status': 'Active'
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = tbl_category
        fields = ['image', 'category_name', 'status']
        widgets = {
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'status': 'Active'
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = tbl_product
        fields = [
            'product_image', 'product_code', 'product_name', 
            'product_price', 'total', 'brand', 
            'category', 'country', 'opening_stock', 
            'closing_stock', 'status'
        ]




class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'address']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            customer = tbl_customer(user=user)
            customer.phone_number = self.cleaned_data['phone_number']
            customer.address = self.cleaned_data['address']
            customer.save()
        return user

class customerloginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)




class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    address = forms.CharField(max_length=255)
    address2 = forms.CharField(max_length=255, required=False)
    country = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=20)
    payment_method = forms.ChoiceField(choices=[('credit', 'Credit card'), ('debit', 'Debit card'), ('paypal', 'PayPal')])
    cc_name = forms.CharField(max_length=100)
    cc_number = forms.CharField(max_length=20)
    cc_expiration = forms.CharField(max_length=5)
    cc_cvv = forms.CharField(max_length=4)


class DeliveryPartnerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    license_number = forms.CharField(max_length=50)
    pan_card_number = forms.CharField(max_length=50)
    aadhaar_number = forms.CharField(max_length=50)
    bike_reg_number = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'license_number', 'pan_card_number', 'aadhaar_number', 'bike_reg_number']

class DeliveryPartnerLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'subject', 'message']


from django import forms
from .models import Subscriber

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
