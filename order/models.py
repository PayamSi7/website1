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

    def __str__(self):
        return self.user.username


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


class OderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'f_name', 'l_name', 'address']