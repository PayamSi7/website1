from django.shortcuts import render, redirect
from home.models import Product
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order.models import OderForm

def cart_detail(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    form = OderForm
    total = 0
    for p in cart:
        if p.product.status != 'None':
            total += p.variant.total_price * p.quantity
        else:
            total += p.product.total_price * p.quantity

    return render(request, 'cart/cart.html', {'cart': cart, 'total': total, 'form': form})

@login_required(login_url='accounts:login')
def add_cart(request, idd):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=idd)
    if product.status != 'None':
        var_id = request.POST.get('select')
        data = Cart.objects.get(user_id=request.user.id, variant_id=var_id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.get(user_id=request.user.id, product_id=idd)
        if data:
            check = 'yes'
        else:
            check = 'no'

    if request.method == 'POST':
        form = CartForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            info = form.cleaned_data['quantity']
            if check == 'yes':
                if product.status != 'None':
                    shop = Cart.objects.get(user_id=request.user.id, product_id=idd, variant_id=var_id)
                    messages.success(request, '.به سبد خرید اضافه شد', 'success')
                else:
                    shop = Cart.objects.get(user_id=request.user.id, product_id=idd)
                shop.quantity += info
                shop.save()
                messages.success(request, '.به سبد خرید اضافه شد', 'success')
            else:
                Cart.objects.create(user_id=request.user.id, product_id=idd, variant_id=var_id, quantity=info)
                messages.success(request, '.به سبد خرید اضافه شد', 'success')
            return redirect(url)


@login_required(login_url='accounts:login')
def remove_cart(request, ids):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=ids).delete()
    return redirect(url)


def add_single(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.product.status == 'None':
        product =Product.objects.get(id=cart.product.id)
        if product.amount > cart.quantity:
            cart.quantity += 1
        else:
            messages.success(request, 'این تعداد در انبار موجود نمی باشد' ,'success')
    else:
        variants =Variants.objects.get(cart.variant.id)
        if variants.amount > cart.quantity:
            cart.quantity += 1
        else:
            messages.success(request, 'این تعداد در انبار موجود نمی باشد' ,'success')
    cart.save()
    return redirect(url)    
                  
def remove_single(request,id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.quantity > 2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)
        
        
        
        
        