from rest_framework import serializers
from .models import*

class CategorySerializer(serializers.ModelSerializerSerializer):
    class Meta:
        model = Category
        fields = ['sub_category', 'sub_cat', 'name', 'create', 'image']