from django.shortcuts import render, redirect
from .models import *
from cart.models import Cart
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm()
    return render(request, 'order/order.html',{'order':order, 'form':form})


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.created(user_id=request.user.id, email=data['email'], f_name=data['f_name'],
                                          l_name=['l-name'], address=data['address'])
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




