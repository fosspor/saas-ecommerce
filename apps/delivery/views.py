from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import DeliveryMethod, DeliveryZone, Shipment
from .serializers import DeliveryMethodSerializer, DeliveryZoneSerializer, ShipmentSerializer
from .services import DeliveryCalculator

class DeliveryMethodListCreateView(generics.ListCreateAPIView):
    serializer_class = DeliveryMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return DeliveryMethod.objects.filter(shop_id=shop_id)
    
    def perform_create(self, serializer):
        shop_id = self.kwargs['shop_id']
        shop = get_object_or_404(Shop, id=shop_id)
        serializer.save(shop=shop)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def calculate_delivery_cost(request):
    delivery_method_id = request.data.get('delivery_method_id')
    from_city = request.data.get('from_city')
    to_city = request.data.get('to_city')
    weight = request.data.get('weight', 1)
    total_amount = request.data.get('total_amount', 0)
    
    try:
        delivery_method = DeliveryMethod.objects.get(id=delivery_method_id)
        cost = DeliveryCalculator.calculate_cost(
            delivery_method, from_city, to_city, weight, total_amount
        )
        return Response({'cost': str(cost)})
    except DeliveryMethod.DoesNotExist:
        return Response({'error': 'Способ доставки не найден'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
