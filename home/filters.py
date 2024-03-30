import django_filters
from django import forms
from .models import*


class ProductFilter(django_filters.FilterSet):
    choice_1 = {
        ('گران ترین','گران ترین')
        ('ارزان ترین','ارزان ترین')
    }
    choice_2 = {
        ('قدیم','قدیم')
        ('جدید ترین','جدید ترین')
    }
    choice_3 = {
        ('کم تخفیف','کم تخفیف')
        ('پرتخفیف','پرتخفیف')
    }
    choice_4 = {
        ('کم فروش','کم فروش')
        ('پرفروش','پرفروش')
    }
    choice_5 = {
        ('کم محبوب','کم محبوب')
        ('محبوب ترین','محبوب ترین')
    }
    price_1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=choice_1, method='price_filter')
    create = django_filters.ChoiceFilter(choices=choice_2, method='create_filter')
    discount = django_filters.ChoiceFilter(choices=choice_3, method='discount_filter')
    sell = django_filters.ChoiceFilter(choices=choice_4, method='sell_filter')
    favorite = django_filters.ChoiceFilter(choices=choice_5, method='favorite_filter')
    
    def price_filter(self,queryset,name,value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)
        
    def create_filter(self,queryset,name,value):
        data = 'create' if value == 'قدیم' else '-create'
        return queryset.order_by(data)
    
    def discount_filter(self,queryset,name,value):
        data = 'discount' if value == 'کم تخفیف' else '-discount'
        return queryset.order_by(data)
        
    def sell_filter(self,queryset,name,value):
        data = 'sell' if value == 'کم فروش' else '-sell'
        return queryset.order_by(data)
        
    def favorite_filter(self,queryset,name,value):
        data = 'total_favorite' if value == 'کم محبوب' else '-total_favorite'
        return queryset.order_by(data)    
        
        
        
        
            
        
        