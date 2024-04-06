from django.shortcuts import render, redirect
from .models import *
from cart.models import Cart
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from suds import Client
from django.http import HttpResponse
from django.utils.crypto import get_random_string
#import ghasedak


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm()
    return render(request, 'order/order.html',{'order':order, 'form':form})


def order_create(request):
    if request.method == 'POST': 
        form = CouponForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            code = get_random_string(length=8)
            order = Order.objects.created(user_id=request.user.id, email=data['email'], f_name=data['f_name'],
                                          l_name=['l-name'], address=data['address'], code=code)
            cart = Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, product_id=c.product_id,
                                         variant_id=c.variant_id, quantity=c.quantity)
            return redirect('order:order_detail', order.id)



def coupon(request, order_id):
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__exist=code, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'this code is wrong', 'danger')
            return redirect('order:order_detail', order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect('order:order_detail', order_id)

"""
#part41
client = Client('#')
#this line will be delete --{amount = 1000  # Rial / Required}
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/order:verify/'
"""

def send_request(request,order_id, price):
    global amount
    amount = price
    """
    result = client.service.PaymentVerification(amount,description,request.user.email, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/Startpay/'+str(result.Authority))
        
    else:
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()
        cart = ItemOrder.objects.filter(order_id=order_id)
        for c in cart:
            if product.status == 'None':
                product = Product.objects.get(id=c.product.id)
                product.sell += c.quantity
                product.save()
                code = order.code
                
                # gasedak code
                # gasedak code
            return HttpResponse('error code: '+str(result.Status))
"""

def verify(request):
    pass
"""
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification( request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted: '+str(result.Status))
        else:
            return HttpResponse('Transaction failed: '+str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
"""

