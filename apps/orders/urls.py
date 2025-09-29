from django.urls import path
from . import views

urlpatterns = [
    path('<int:shop_id>/orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:shop_id>/orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('cart/', views.cart_detail, name='cart-detail'),
    path('cart/items/<int:item_id>/', views.cart_item_delete, name='cart-item-delete'),
]
