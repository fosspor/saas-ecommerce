from django.urls import path
from . import views

urlpatterns = [
    path('<int:shop_id>/payment-methods/', views.PaymentMethodListCreateView.as_view(), 
         name='payment-method-list-create'),
    path('<int:shop_id>/orders/<int:order_id>/create-payment/', 
         views.create_payment_for_order, name='create-payment-for-order'),
]
