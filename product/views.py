from django.shortcuts import render

from .serializers import CategorySerializer, ProductSerializer
from .models import Product, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from rest_framework.decorators import api_view
from django.db.models import Q

class LatestProductlist(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, product_slug):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    
    if query:
        products = Product.object.filter(Q(name_icontains=query) | Q(description_icontains = query))
        serializer = CategorySerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products': []})