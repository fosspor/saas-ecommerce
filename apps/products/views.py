from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Category, Product, ProductImage, ProductVariant
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, ProductVariantSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Category.objects.filter(shop_id=shop_id)
    
    def perform_create(self, serializer):
        shop_id = self.kwargs['shop_id']
        shop = get_object_or_404(Shop, id=shop_id)
        serializer.save(shop=shop)

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Product.objects.filter(shop_id=shop_id)
    
    def perform_create(self, serializer):
        shop_id = self.kwargs['shop_id']
        shop = get_object_or_404(Shop, id=shop_id)
        serializer.save(shop=shop)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Product.objects.filter(shop_id=shop_id)
