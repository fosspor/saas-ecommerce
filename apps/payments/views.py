from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PaymentMethod, Payment
from .serializers import PaymentMethodSerializer, PaymentSerializer
from .services import PaymentService

class PaymentMethodListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return PaymentMethod.objects.filter(shop_id=shop_id)
    
    def perform_create(self, serializer):
        shop_id = self.kwargs['shop_id']
        shop = get_object_or_404(Shop, id=shop_id)
        serializer.save(shop=shop)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_payment_for_order(request, shop_id, order_id):
    order = get_object_or_404(Order, id=order_id, shop_id=shop_id)
    payment_method_id = request.data.get('payment_method_id')
    return_url = request.data.get('return_url')
    
    if not payment_method_id or not return_url:
        return Response({'error': 'Необходимо указать способ оплаты и URL возврата'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    payment_method = get_object_or_404(PaymentMethod, id=payment_method_id, shop_id=shop_id)
    
    try:
        payment = PaymentService.create_payment_for_order(order, payment_method, return_url)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
