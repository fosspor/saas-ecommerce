from rest_framework import serializers
from .models import PromoCode, EmailTemplate, EmailCampaign, Review

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['id', 'code', 'name', 'description', 'discount_type', 'discount_value',
                 'minimum_order_amount', 'usage_limit', 'usage_count', 'is_active',
                 'valid_from', 'valid_until', 'created_at', 'updated_at']

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'type', 'subject', 'content', 'is_active', 
                 'created_at', 'updated_at']

class EmailCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCampaign
        fields = ['id', 'name', 'template', 'status', 'target_customers', 'target_segments',
                 'scheduled_at', 'sent_at', 'total_recipients', 'sent_count', 
                 'opened_count', 'clicked_count', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'customer', 'customer_name', 'order', 'rating', 
                 'title', 'content', 'is_approved', 'is_verified_purchase', 
                 'created_at', 'updated_at']
