from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from .forms import*
from django.db.models import Q
from cart.models import *
from django.core.mail import EmailMessage
from django.core.paginator import Paginator


def home(request):
    category = Category.objects.filter(sub_cat=True)
    return render(request, 'home/home.html', {'category': category})

def All_product(request, slug=None, id= None):
    products = Product.objects.all()
    paginator = Paginator(products, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    s_form = SearchForm()
    category = Category.objects.filter(sub_cat=False)
    form = SearchForm
    if 'search' in request.GET:
        form = SearchForm(request.POST)
        if form.is_valid:
            dataa = form.cleaned_data['search']
            products = products.filter(name__icontains=dataa)
    category = Category.objects.filter(sub_cat=True)
    if slug and id:
        data = get_object_or_404(Category, slug=slug, id=id)
        page_obj = products.filter(category=data)
        paginator = Paginator(page_obj, 3)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
    return render(request, 'home/products.html', {'products': page_obj, 'category': category,'form':form})

def Product_detail(request,id=None):
    product = get_object_or_404(Product, id=id)
    image = Images.objects.filter(product_id=id)
    comment_form = CommentForm()
    cart_form = CartForm()
    comment = Comment.objects.filter(product_id=id, is_reply=False)
    reply_form = ReplyForm()
    similar = product.tags.similar_objects()[:2]
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True

    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = False
    
    is_favorite = False
    if Product.favorite.filter(id=request.user.id).exists():
        is_favorite = True
        
    if product.status is not None:
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            variants = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant[0].id)
        cont = {'product': product, 'variant': variant, 'variants': variants, 'similar': similar, 'is_like': is_like,
                'is_unlike': is_unlike, 'comment_form': comment_form,'comment': comment, 'reply_form': reply_form,
                'image': image, 'cart_form': cart_form, 'is_favorite': is_favorite}
        return render(request, 'home/detail.html', cont)

    else:
        return render(request, 'home/detail.html', {'product': product, 'similar': similar,'is_favorite': is_favorite,
                                                    'is_like': is_like, 'is_unlike': is_unlike, 'comment': comment,
                                                    'comment_form': comment_form, 'reply_form': reply_form,
                                                    'image': image, 'cart_form': cart_form})



def product_like(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
        messages.success(request, 'remove', 'success')
    else:
        product.like.add(request.user)
        is_like = True
        messages.success(request,'خوشحالیم که مورد پسند شما بود', 'success')
    return redirect(url)

def product_unlike(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        product.unlike.remove(request.user)
        is_unlike = False
        messages.success(request, 'remove dislike', 'success')
    else:
        product.unlike.add(request.user)
        is_unlike = True
        messages.success(request,'add dislike', 'success')
    return redirect(url)


def product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'], rate=data['rate'], user_id=request.user.id, product_id=id)
        return redirect(url)

def product_reply(request, comment_id,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(comment=data['comment'], user_id=request.user.id, product_id=id,
                                   reply_id=comment_id, is_reply=True)
            messages.success(request,'thank you', 'primary')
            return redirect(url)
        #else:
         #   return redirect(url)

def comment_like(request,id):
    url = request.META.get('HTTP-REFERER')
    comment = Comment.objects.get(id=id)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
    else:
        comment.comment_like.add(request.user)
        messages.success(request, 'thank', 'warning')
    return redirect(url)


def product_search(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        #    if data.isdigit():
        #        products = products.filter(Q(discount__exast=data['search']) | Q(unit_price__exast=data['search']))
        #   else:
            products = products.filter(name__icontains=data['search'])
            return render(request, 'home/product.html', {'products':products, 'form':form})
    else:
        pass
        

def favorite_product(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.filter(id=id)
    is_favorite = False
    if Product.favorite.filter(id=request.user.id).exists():
        Product.favorite.remove(request.user)
        is_favorite = False
    else:
        Product.favorite.add(request.user)
        is_favorite = True
    return redirect(url)

def contact(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        msg = request.POST['measage']
        body = subject + '\n' + email + '\n' + msg
        form = EmailMessage(
            'contact form',#email title
            body,#email text
            'test',#
            ('',),#your email address 
        )
        form.send(fail_silently=False)
    return render(request, 'home/contact.html')







