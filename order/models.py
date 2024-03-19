from django.db import models
from django.contrib.auth.models import User
from home.models import *
from django.forms import ModelForm


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    email = models.EmailField()
    f_name = models.CharField(max_length=200)
    l_name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    discount = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def cost(self):
        total = sum( i.price() for i in self.order_item.all())
        return total

class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

    def size(self):
        return self.variant.Size_variant.name

    def color(self):
        return self.variant.Color_variant.name

    def price(self):
        if self.product.status != 'None':
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity

class OderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'f_name', 'l_name', 'address']
        
        
class Coupon(models.Model):
    code = models.CharField(max_length=110)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.IntegerField()
    
        
        
        
        
        
        
        
        
        
        
        