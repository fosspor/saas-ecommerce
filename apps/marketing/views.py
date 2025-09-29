from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import PromoCode, EmailTemplate, EmailCampaign, Review
from .serializers import PromoCodeSerializer, EmailTemplateSerializer, EmailCampaignSerializer, ReviewSerializer

class PromoCodeListCreateView(generics.ListCreateAPIView):
    serializer_class = PromoCodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return PromoCode.objects.filter(shop_id=shop_id)
    
    def perform_create(self, serializer):
        shop_id = self.kwargs['shop_id']
        shop = get_object_or_404(Shop, id=shop_id)
        serializer.save(shop=shop)

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Review.objects.filter(shop_id=shop_id)
    
    def perform_create(self, serializer):
        shop_id = self.kwargs['shop_id']
        shop = get_object_or_404(Shop, id=shop_id)
        serializer.save(shop=shop)
