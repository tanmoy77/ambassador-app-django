from core.models import Product
from .serializers import ProductSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.core.cache import cache 


class ProductFrontendAPIView(APIView):
    @method_decorator(cache_page(60 * 60 * 2, key_prefix='products_frontend'))
    def get(self, _):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductBackendAPIView(APIView):
    def get(self, _):
        products = cache.get('products_backend')

        if not products:
            products = list(Product.objects.all())
            cache.set('products_backend', products, timeout=60*30) #30 min
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
