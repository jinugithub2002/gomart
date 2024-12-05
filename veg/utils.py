from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_assignment_email(order, delivery_partner, shipping_info):
    subject = f"Order Assignment: Order ID {order.id}"
    message = render_to_string('order_assignment_email.html', {
        'order': order,
        'delivery_partner': delivery_partner,
        'shipping_info': shipping_info,
    })

    plain_message = f"""
    Order Assignment Details
    Dear {delivery_partner.user.first_name},
    
    You have been assigned a new order. Here are the details:
    
    Order ID: {order.id}
    Customer: {order.user.first_name} {order.user.last_name}
    Order Date: {order.order_date}
    Total Amount: {order.total_amount}
    
    Items:
    """
    for item in order.items.all():
        total_price = item.product.product_price * item.quantity  # Compute total price dynamically
        plain_message += f"{item.product.product_name} x {item.quantity} = {total_price}\n"

    plain_message += "Shipping Information:\n"
    if shipping_info:
        plain_message += f"""
        Name: {shipping_info.first_name} {shipping_info.last_name}
        Email: {shipping_info.email}
        Address: {shipping_info.address}
        {shipping_info.address2}
        {shipping_info.city}, {shipping_info.state}, {shipping_info.zip_code}
        Country: {shipping_info.country}
        """
    else:
        plain_message += "No shipping information available."

    plain_message += "\nThank you!"

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [delivery_partner.user.email],
        fail_silently=False,
        html_message=message,  # Ensure the HTML content is sent
    )


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_thank_you_email(inquiry):
    subject = "Thank You for Contacting Us"
    message = render_to_string('thank_you_email.html', {
        'inquiry': inquiry,
    })
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [inquiry.email],
        fail_silently=False,
        html_message=message,  # Ensure the HTML content is sent
    )


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_thank_you_email(subscriber):
    subject = "Thank You for Subscribing to VegMart"
    message = render_to_string('thank_you_email.html', {
        'subscriber': subscriber,
    })
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [subscriber.email],
        fail_silently=False,
        html_message=message,  # Ensure the HTML content is sent
    )

def send_new_item_notification(subscriber, product):
    subject = "New Item Arrived at VegMart"
    message = render_to_string('new_item_notification.html', {
        'subscriber': subscriber,
        'product': product,
    })
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [subscriber.email],
        fail_silently=False,
        html_message=message,  # Ensure the HTML content is sent
    )


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Subscriber

def send_email_to_all_subscribers(subject, message):
    subscribers = Subscriber.objects.all()
    recipient_list = [subscriber.email for subscriber in subscribers]
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )
