from rest_framework import serializers
from .models import Shop, ShopMember, Page

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'domain', 'description', 'theme', 'is_active', 'created_at']
        read_only_fields = ['created_at']

class ShopMemberSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ShopMember
        fields = ['id', 'user', 'user_username', 'role', 'created_at']
        read_only_fields = ['created_at']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'content', 'page_type', 'is_published', 
                 'seo_title', 'seo_description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
