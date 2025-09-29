from django.urls import path
from . import views

urlpatterns = [
    path('<int:shop_id>/promo-codes/', views.PromoCodeListCreateView.as_view(), 
         name='promo-code-list-create'),
    path('<int:shop_id>/reviews/', views.ReviewListCreateView.as_view(), 
         name='review-list-create'),
]
