from rest_framework import serializers 
from core.models import Link, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = '__all__'

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'