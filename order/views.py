from django.shortcuts import render, redirect
from .models import *
from cart.models import Cart
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order/order.html',{'order':order})


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

