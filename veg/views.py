from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import tbl_country,tbl_brands,tbl_category,tbl_product ,Wishlist,CartItem, Order,WishlistItem,OrderItem, ShippingInfo ,DeliveryPartner
from .forms import TblCountryForm,BrandForm,CategoryForm,ProductForm,CustomerRegistrationForm, customerloginForm,CheckoutForm,UserRegistrationForm, LoginForm, DeliveryPartnerRegistrationForm, DeliveryPartnerLoginForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail  
import razorpay
from django.conf import settings



@login_required
def index(request):
    user = None
    cat= tbl_category.objects.all() 
    products = tbl_product.objects.all()
    fruits = tbl_product.objects.filter(category__category_name="Fruits")
    vegetables = tbl_product.objects.filter(category__category_name="vegetables")
    if 'user_id' in request.session: 
        user = User.objects.get(id=request.session['user_id'])
    return render(request, 'index.html', {'cat': cat,'products': products ,'vegetables': vegetables, 'fruits': fruits,'user': user}) 


def cart(request):
    return render(request, 'cart.html')


def shop_detail(request):
    return render(request,'shop-detail.html')
    
def shop(request):
    return render(request,'shop.html')

def error(request):
    return render(request,'404.html')

def testimonial(request):
    return render(request,'testimonial.html')




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send welcome email
            send_mail(
                'Welcome to VegMart',
                'Hello {},\n\nThank you for registering at VegMart! We are excited to have you on board.\n\nBest regards,\nVegMart Team'.format(user.username),
                'your-email@example.com',  # From email
                [user.email],  # To email
                fail_silently=False,
            )

            # Store a success message in the session
            request.session['registration_success'] = 'Your registration was successful! A welcome email has been sent to your registered email address.'
            return redirect('registration_success')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})



    
def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  
            else:
                error_message = 'Invalid credentials'
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    return render(request, 'dashboard.html')


def country_list(request):
    countries = tbl_country.objects.all()
    return render(request, 'country_list.html', {'countries': countries})

def country_edit(request, pk):
    country = get_object_or_404(tbl_country, pk=pk)
    if request.method == 'POST':
        form = TblCountryForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('country_list')
    else:
        form = TblCountryForm(instance=country)
    return render(request, 'country_edit.html', {'form': form})

def country_add(request):
    if request.method == 'POST':
        form = TblCountryForm(request.POST) 
        if form.is_valid():
           form.save() 
        return redirect('country_list') 
    else: form = TblCountryForm()
    return render(request, 'country_add.html', {'form': form})

def country_delete(request, pk):
    country = get_object_or_404(tbl_country, pk=pk)
    if request.method == 'POST':
        country.delete()
        return redirect('country_list')
    return render(request, 'country_confirm_delete.html', {'country': country})




# View to list all brands
def brand_list(request):
    brands = tbl_brands.objects.all()
    return render(request, 'brand_list.html', {'brands': brands})

# View to add a new brand
def brand_add(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
    else:
        form = BrandForm()
    return render(request, 'brand_add.html', {'form': form})

# View to edit an existing brand
def brand_edit(request, pk):
    brand = get_object_or_404(tbl_brands, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'brand_edit.html', {'form': form})

# View to delete a brand
def brand_delete(request, pk):
    brand = get_object_or_404(tbl_brands, pk=pk)
    if request.method == 'POST':
        brand.delete()
        return redirect('brand_list')
    return render(request, 'brand_confirm_delete.html', {'brand': brand})



def category_list(request):
    categories = tbl_category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_add.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(tbl_category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_edit.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(tbl_category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})


def product_list(request):
    query = request.GET.get('q')
    products = tbl_product.objects.all()

    if query:
        products = products.filter(
            Q(product_code__icontains=query) |
            Q(product_name__icontains=query) |
            Q(brand__brand_name__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(country__country_name__icontains=query) |
            Q(product_price__icontains=query) |
            Q(opening_stock__icontains=query) |
            Q(closing_stock__icontains=query) |
            Q(status__icontains=query)
        )

    return render(request, 'product_list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_add.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(tbl_product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_edit.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(tbl_product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})



def product_search(request):
    query = request.GET.get('q', '')
    products = tbl_product.objects.filter(
        Q(product_code__icontains=query) |
        Q(product_name__icontains=query) |
        Q(brand__brand_name__icontains=query) |
        Q(category__category_name__icontains=query) |
        Q(country__country_name__icontains=query)
    )
    results = []
    for product in products:
        results.append({
            'product_image': product.product_image.url,
            'product_name': product.product_name
        })
    return JsonResponse(results, safe=False)


def all_products(request):
    products = tbl_product.objects.all()
    brands = tbl_brands.objects.all()
    return render(request, 'all_products.html', {'products': products, 'brands': brands})


def category_products(request, category_id):
    category = get_object_or_404(tbl_category, id=category_id)
    products = tbl_product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})





@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = Wishlist.objects.get(id=item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')

@login_required
def wishlist(request):
    user = User.objects.get(id=request.session['user_id'])
    wishlist_items = WishlistItem.objects.filter(user=user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_all_to_cart(request):
    user = User.objects.get(id=request.session['user_id'])
    wishlist_items = WishlistItem.objects.filter(user=user)
    for item in wishlist_items:
        cart_item, created = CartItem.objects.get_or_create(user=user, product=item.product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
    wishlist_items.delete()  # Clear wishlist after adding to cart
    return redirect('view_cart')


@login_required
def add_to_wishlist(request, product_id):
    user = User.objects.get(id=request.session['user_id'])
    product = tbl_product.objects.get(id=product_id)
    WishlistItem.objects.get_or_create(user=user, product=product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = WishlistItem.objects.get(id=item_id)
    wishlist_item.delete()
    return redirect('wishlist')






def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer_registration.html', {'form': form})



def customer_login(request):
    error_message = None
    if request.method == 'POST':
        form = customerloginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['user_id'] = user.id  # Store user ID in session

                # Send welcome email
                send_mail(
                    'Welcome to VegMart',
                    'Hello {},\n\nWelcome back to VegMart! We are glad to have you with us.\n\nBest regards,\nVegMart Team'.format(user.username),
                    'your-email@example.com',  
                    [user.email],  
                    fail_silently=False,
                )

                return redirect('index')  # Redirect to products page after login
            else:
                error_message = 'Invalid credentials'
    else:
        form = LoginForm()
    return render(request, 'customer_login.html', {'form': form, 'error_message': error_message})


def customer_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user ID from session
    return redirect('customer_logout')


def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        return redirect('customer_login')  # Redirect to login if user is not authenticated

    product = tbl_product.objects.get(id=product_id)
    user = User.objects.get(id=request.session['user_id'])
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')



def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.session['user_id'])
    total_amount = 0

    
    # Calculate the total amount for each item in the cart
    for item in cart_items:
        item.total_price = item.product.product_price * item.quantity
        total_amount += item.total_price
    
    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })



def remove_from_cart(request, item_id):
    if 'user_id' not in request.session:
        return redirect('customer_login')  # Redirect to login if user is not authenticated

    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def update_cart_item(request, item_id):
    if 'user_id' not in request.session:
        return redirect('customer_login')  # Redirect to login if user is not authenticated

    cart_item = CartItem.objects.get(id=item_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart_item.quantity = int(quantity)
        cart_item.save()
    return redirect('view_cart')


import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CartItem, Order, OrderItem, ShippingInfo
from .forms import CheckoutForm

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

@login_required
def checkout(request):
    if 'user_id' not in request.session:
        return redirect('customer_login')  # Redirect to login if user is not authenticated

    cart_items = CartItem.objects.filter(user=request.session['user_id'])
    total_amount = sum(float(item.product.product_price) * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Minimum amount check (assume 1 INR as minimum amount for example)
            if total_amount < 1.00:
                return render(request, 'checkout.html', {
                    'form': form,
                    'cart_items': cart_items,
                    'total_amount': total_amount,
                    'error_message': 'Order amount is less than the minimum amount allowed.'
                })

            order = Order.objects.create(user=request.user, total_amount=total_amount)
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            cart_items.delete()  # Clear cart after checkout

            # Save shipping information
            ShippingInfo.objects.create(
                order=order,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                address2=form.cleaned_data['address2'],
                country=form.cleaned_data['country'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code']
            )

            # Create Razorpay order
            amount1 = int(total_amount * 100)  # Convert amount to paise
            if amount1 < 100:  # Assuming 100 paise is the minimum order amount
                return render(request, 'checkout.html', {
                    'form': form,
                    'cart_items': cart_items,
                    'total_amount': total_amount,
                    'error_message': 'Order amount is less than the minimum amount allowed by Razorpay.'
                })

            razorpay_order = razorpay_client.order.create({
                'amount': amount1,
                'currency': 'INR',
                'payment_capture': '1'
            })
            order_id = razorpay_order['id']

            context = {
                       'form': form,
                       'cart_items': cart_items_with_totals,
                       'total_amount': total_amount,  # Total amount in INR (for display)
                       'amount_in_paise': float(total_amount * 100),  # Total amount in paise (for Razorpay)
                       'razorpay_merchant_key': settings.RAZORPAY_API_KEY,
                       'order_id': order_id,
                        'currency': 'INR',
}
            return render(request, 'checkout.html', context)

    else:
        form = CheckoutForm()

    cart_items_with_totals = [
        {
            'item': item,
            'quantity': item.quantity,
            'item_total': float(item.product.product_price) * item.quantity
        }
        for item in cart_items
    ]

    context = {
        'form': form,
        'cart_items': cart_items_with_totals,
        'total_amount': total_amount,  # Pass the total amount
        'razorpay_merchant_key': settings.RAZORPAY_API_KEY
    }
    return render(request, 'checkout.html', context)




@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        try:
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            razorpay_signature = data['razorpay_signature']

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            # Verify the payment signature
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is None:
                # Payment verification successful
                order = Order.objects.get(order_id=razorpay_order_id)
                order.payment_id = razorpay_payment_id
                order.status = 'Paid'
                order.save()

                # Fetch shipping info
                shipping_info = ShippingInfo.objects.get(order=order)

                # Redirect to the invoice view with order details
                return redirect('invoice.html', {'order': order, 'shipping_info': shipping_info})
            else:
                return render(request, 'payment_failure.html')

        except Exception as e:
            return render(request, 'payment_failure.html')
    else:
        return render(request, 'payment_failure.html')

from django.shortcuts import render, get_object_or_404
from .models import Order, ShippingInfo

def invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    try:
        shipping_info = ShippingInfo.objects.get(order=order)
    except ShippingInfo.DoesNotExist:
        shipping_info = None
    
    order_items = []
    for item in order.items.all():
        item_total_price = item.product.product_price * item.quantity
        order_items.append({
            'product_name': item.product.product_name,
            'product_image_url': item.product.product_image.url,
            'quantity': item.quantity,
            'product_price': item.product.product_price,
            'total_price': item_total_price
        })
    
    return render(request, 'invoice.html', {
        'order': order,
        'shipping_info': shipping_info,
        'order_items': order_items,
    })


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order,id=request.session['user_id'])
    order_items = OrderItem.objects.filter(order=order)
    order_items_with_totals = [
        {
            'product': item.product,
            'quantity': item.quantity,
            'product_image': item.product.product_image.url,
            'item_total': float(item.product.product_price) * item.quantity
        }
        for item in order_items
    ]
    context = {
        'order': order,
        'order_items': order_items_with_totals
    }
    return render(request, 'order_confirmation.html', context)



def order_list(request):
    if 'user_id' not in request.session:
        return redirect('customer_login')  # Redirect to login if user is not authenticated

    user = get_object_or_404(User, id=request.session['user_id'])
    orders = Order.objects.filter(user=user)

    # Compute total price for each order item
    for order in orders:
        for item in order.items.all():
            item.total_price = item.product.product_price * item.quantity

    return render(request, 'order_list.html', {'orders': orders})


def products(request):
    products = tbl_product.objects.all()
    return render(request, 'products.html', {'products': products})


def pending_orders(request):
    pending_orders = Order.objects.filter(status='Pending')

    # Compute total price for each order item and prepare the context data
    for order in pending_orders:
        for item in order.items.all():
            item.total_price = item.product.product_price * item.quantity

    return render(request, 'pending_orders.html', {'pending_orders': pending_orders})

def verify_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = 'Delivered'
        order.save()
        return redirect('pending_orders')
    return render(request, 'verify_order.html', {'order': order})



def delivery_partner_register(request):
    if request.method == 'POST':
        form = DeliveryPartnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            license_number = form.cleaned_data.get('license_number')
            pan_card_number = form.cleaned_data.get('pan_card_number')
            aadhaar_number = form.cleaned_data.get('aadhaar_number')
            bike_reg_number = form.cleaned_data.get('bike_reg_number')
            delivery_partner = DeliveryPartner(
                user=user,
                license_number=license_number,
                pan_card_number=pan_card_number,
                aadhaar_number=aadhaar_number,
                bike_reg_number=bike_reg_number
            )
            delivery_partner.save()
            login(request, user)
            return redirect('delivery_dashboard')
    else:
        form = DeliveryPartnerRegistrationForm()
    return render(request, 'delivery_partner_register.html', {'form': form})

def delivery_partner_login_view(request):
    if request.method == 'POST':
        form = DeliveryPartnerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('delivery_dashboard')
    else:
        form = DeliveryPartnerLoginForm()
    return render(request, 'delivery_login.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DeliveryPartner, Order, ShippingInfo

@login_required
def delivery_dashboard(request):
    try:
        delivery_partner = DeliveryPartner.objects.get(user=request.user)
        new_orders = Order.objects.filter(delivery_partner=delivery_partner, status='Pending')
        completed_orders = Order.objects.filter(delivery_partner=delivery_partner, status='Delivered')

        # Compute total price for each order item
        for order in new_orders:
            for item in order.items.all():
                item.total_price = item.product.product_price * item.quantity

        for order in completed_orders:
            for item in order.items.all():
                item.total_price = item.product.product_price * item.quantity

        # Fetch shipping information
        order_shipping_info = []
        for order in new_orders:
            try:
                shipping_info = ShippingInfo.objects.get(order=order)
            except ShippingInfo.DoesNotExist:
                shipping_info = None
            order_shipping_info.append({
                'order': order,
                'shipping_info': shipping_info,
                'status': 'new',
            })
        for order in completed_orders:
            try:
                shipping_info = ShippingInfo.objects.get(order=order)
            except ShippingInfo.DoesNotExist:
                shipping_info = None
            order_shipping_info.append({
                'order': order,
                'shipping_info': shipping_info,
                'status': 'completed',
            })

        return render(request, 'delivery_dashboard.html', {
            'delivery_partner': delivery_partner,
            'order_shipping_info': order_shipping_info,
        })
    except DeliveryPartner.DoesNotExist:
        return redirect('delivery_register')  # Redirect to registration page if delivery partner does not exist



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, DeliveryPartner, ShippingInfo
from .utils import send_order_assignment_email

@login_required
def assign_orders(request):
    if request.method == 'POST':
        delivery_partner_id = request.POST.get('delivery_partner')
        order_ids = request.POST.getlist('order_ids')

        delivery_partner = get_object_or_404(DeliveryPartner, id=delivery_partner_id)

        for order_id in order_ids:
            order = get_object_or_404(Order, id=order_id)
            order.delivery_partner = delivery_partner
            order.save()

            # Compute total price for each order item
            for item in order.items.all():
                item.total_price = item.product.product_price * item.quantity
            
            # Check for ShippingInfo existence
            try:
                shipping_info = ShippingInfo.objects.get(order=order)
            except ShippingInfo.DoesNotExist:
                shipping_info = None
            
            send_order_assignment_email(order, delivery_partner, shipping_info)  # Pass shipping_info to email function

        return redirect('assign_orders')

    pending_orders = Order.objects.filter(status='Pending', delivery_partner__isnull=True)
    delivery_partners = DeliveryPartner.objects.all()

    return render(request, 'assign_orders.html', {
        'pending_orders': pending_orders,
        'delivery_partners': delivery_partners,
    })



@login_required
def assigned_orders(request):
    try:
        delivery_partner = DeliveryPartner.objects.get(user=request.user)
        orders = Order.objects.filter(delivery_partner=delivery_partner)

        for order in orders:
            for item in order.items.all():
                item.total_price = item.product.product_price * item.quantity

        return render(request, 'assigned_orders.html', {'orders': orders})
    except DeliveryPartner.DoesNotExist:
        return redirect('delivery_register')  # Redirect to a registration page or show an error message


from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('delivery_dashboard')


from django.shortcuts import render, redirect
from .forms import InquiryForm
from .models import Inquiry
from .utils import send_thank_you_email

def contact_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            send_thank_you_email(inquiry)  # Send thank you email
            return redirect('contact_thank_you')  # Redirect to a thank you page or display a success message
    else:
        form = InquiryForm()
    return render(request, 'contact.html', {'form': form})

def enquiries_view(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'enquiries.html', {'inquiries': inquiries})

def contact_thank_you(request):
    return render(request, 'contact_thank_you.html')



from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Order, DeliveryPartner

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def shipping_management(request):
    pending_orders = Order.objects.filter(status='Pending').select_related('delivery_partner')
    completed_orders = Order.objects.filter(status='Delivered').select_related('delivery_partner')

    return render(request, 'shipping_management.html', {
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
    })



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SubscriptionForm
from .utils import send_thank_you_email

@require_POST
def subscribe_view(request):
    form = SubscriptionForm(request.POST)
    if form.is_valid():
        subscriber = form.save()
        send_thank_you_email(subscriber)  # Send thank you email
        return JsonResponse({"message": "Thank you for subscribing!"})
    else:
        return JsonResponse({"errors": form.errors.as_json()}, status=400)



def subscription_thank_you(request):
    return render(request, 'subscription_thank_you.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import send_email_to_all_subscribers
from .models import Subscriber

def view_subscribers(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'view_subscribers.html', {'subscribers': subscribers})

def send_email_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_email_to_all_subscribers(subject, message)
        messages.success(request, 'Email sent to all subscribers.')
        return redirect('view_subscribers')
    return render(request, 'send_email.html')



def view_customers(request):
    customers = User.objects.all()
    return render(request, 'view_customers.html', {'customers': customers})




def order_history_view(request):
    delivered_orders = Order.objects.filter(status='Delivered').select_related('user')
    pending_orders = Order.objects.filter(status='Pending').select_related('user')

    # Compute total price for each order item
    for order in delivered_orders:
        for item in order.items.all():
            item.total_price = item.product.product_price * item.quantity
    
    for order in pending_orders:
        for item in order.items.all():
            item.total_price = item.product.product_price * item.quantity

    return render(request, 'order_history.html', {
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import  Feedback
from django.contrib import messages

def submit_feedback(request, product_id):
    product = get_object_or_404(tbl_product, id=product_id)
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        Feedback.objects.create(product=product, text=feedback_text)
        messages.success(request, 'Thank you for your feedback!')
    return redirect('order_history')


def feedback_view(request):
    feedbacks = Feedback.objects.select_related('product').all()
    return render(request, 'feedback.html', {'feedbacks': feedbacks})



import os
import shutil
from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render

def download_db(request):
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    if os.path.exists(db_path):
        with open(db_path, 'rb') as db_file:
            response = HttpResponse(db_file.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = 'attachment; filename=db.sqlite3'
            return response
    raise Http404

def download_images(request):
    images_dir = os.path.join(settings.BASE_DIR, 'media')
    zip_path = os.path.join(settings.BASE_DIR, 'media.zip')
    
    if os.path.exists(images_dir):
        shutil.make_archive('media', 'zip', images_dir)
        with open(zip_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=media.zip'
            return response
    raise Http404

def download_page(request):
    return render(request, 'download.html')
