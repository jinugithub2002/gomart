from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class tbl_user_reg(models.Model):
    username=models.CharField(max_length=100 ,null=True)
    email=models.EmailField(max_length=100 ,null=True)
    mobile=models.IntegerField(null=True)
    password=models.CharField(max_length=100 ,null=True)
    
class tbl_country(models.Model):
    country_name = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)  # True for Active, False for Inactive
    
    def __str__(self):
        return self.country_name


class tbl_brands(models.Model):
    logo= models.ImageField(upload_to="media",null=True ,blank=True)
    brand_name = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)  # True for Active, False for Inactive
    
    def __str__(self):
        return self.brand_name

class tbl_category(models.Model):
    image = models.ImageField(upload_to='media', null=True, blank=True)
    category_name = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)  # True for Active, False for Inactive

    def __str__(self):
        return self.category_name
    
class tbl_product(models.Model):
    product_image = models.ImageField(upload_to='media', null=True, blank=True)
    product_code = models.CharField(max_length=100, null=True)
    product_name = models.CharField(max_length=100, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total=models.FloatField(max_length=100, null=True)
    brand = models.ForeignKey(tbl_brands, on_delete=models.CASCADE)
    category = models.ForeignKey(tbl_category, on_delete=models.CASCADE)
    country = models.ForeignKey(tbl_country, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    opening_stock = models.IntegerField()
    closing_stock = models.IntegerField()
    status = models.BooleanField(default=True)
    
    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"




class tbl_customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    
    


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"
    




class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey('DeliveryPartner', on_delete=models.SET_NULL, null=True, blank=True)  # Add this line
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"



class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(tbl_product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} added to wishlist by {self.user.username}"



class ShippingInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"ShippingInfo for Order {self.order.id}"


class DeliveryPartner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    pan_card_number = models.CharField(max_length=50)
    aadhaar_number = models.CharField(max_length=50)
    bike_reg_number = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.license_number}"




class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name} - {self.subject}"



from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Feedback(models.Model):
    product = models.ForeignKey(tbl_product, related_name='feedback', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
