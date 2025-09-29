from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Shop, ShopMember, Page
from .serializers import ShopSerializer, ShopMemberSerializer, PageSerializer

class ShopListCreateView(generics.ListCreateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_shop_admin:
            return Shop.objects.all()
        return Shop.objects.filter(members__user=self.request.user)
    
    def perform_create(self, serializer):
        shop = serializer.save(owner=self.request.user)
        # Добавляем владельца как администратора магазина
        ShopMember.objects.create(
            shop=shop,
            user=self.request.user,
            role='admin'
        )

class ShopDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_shop_admin:
            return Shop.objects.all()
        return Shop.objects.filter(members__user=self.request.user)

class ShopMemberListView(generics.ListCreateAPIView):
    serializer_class = ShopMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return ShopMember.objects.filter(shop_id=shop_id)
    
    def perform_create(self, serializer):
        shop_id = self.kwargs['shop_id']
        shop = get_object_or_404(Shop, id=shop_id)
        serializer.save(shop=shop)

class PageListCreateView(generics.ListCreateAPIView):
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Page.objects.filter(shop_id=shop_id)
    
    def perform_create(self, serializer):
        shop_id = self.kwargs['shop_id']
        shop = get_object_or_404(Shop, id=shop_id)
        serializer.save(shop=shop)

class PageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Page.objects.filter(shop_id=shop_id)
