from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Count
from apps.shops.models import Shop
from apps.orders.models import Order
from apps.products.models import Product
from apps.users.models import User

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_dashboard_stats(request):
    total_shops = Shop.objects.count()
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    
    # Выручка за последние 30 дней
    from django.utils import timezone
    from datetime import timedelta
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_revenue = Order.objects.filter(
        created_at__gte=thirty_days_ago,
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Заказы по статусам
    orders_by_status = Order.objects.values('status').annotate(count=Count('id'))
    
    return Response({
        'total_shops': total_shops,
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'recent_revenue': float(recent_revenue),
        'orders_by_status': list(orders_by_status)
    })

class ShopListView(generics.ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return Shop.objects.all().select_related('owner')
