from rest_framework import serializers
from .models import Order, OrderItem, Cart, CartItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_sku', 'quantity', 'price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer_email', 'customer_phone', 'customer_first_name',
                 'customer_last_name', 'shipping_address_line1', 'shipping_address_line2',
                 'shipping_city', 'shipping_state', 'shipping_postcode', 'shipping_country',
                 'billing_address_line1', 'billing_address_line2', 'billing_city',
                 'billing_state', 'billing_postcode', 'billing_country', 'currency',
                 'subtotal', 'shipping_cost', 'tax_amount', 'discount_amount', 'total_amount',
                 'status', 'payment_status', 'notes', 'created_at', 'updated_at', 'items']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'total_amount', 'created_at', 'updated_at']
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    
    def get_total_amount(self, obj):
        return sum(item.total_price for item in obj.items.all())
