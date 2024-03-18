from django.contrib import admin
from .models import *

class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user', 'product', 'variant', 'size', 'color', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'f_name', 'l_name', 'address', 'create', 'paid']
    inlines = [ItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrder)
