from django.urls import path
from . import views

urlpatterns = [
    path('<int:shop_id>/delivery-methods/', views.DeliveryMethodListCreateView.as_view(), 
         name='delivery-method-list-create'),
    path('calculate-cost/', views.calculate_delivery_cost, name='calculate-delivery-cost'),
]
