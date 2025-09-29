from django.urls import path
from . import views

urlpatterns = [
    path('<int:shop_id>/categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('<int:shop_id>/products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:shop_id>/products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]
