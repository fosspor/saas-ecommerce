from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopListCreateView.as_view(), name='shop-list-create'),
    path('<int:pk>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('<int:shop_id>/members/', views.ShopMemberListView.as_view(), name='shop-member-list'),
    path('<int:shop_id>/pages/', views.PageListCreateView.as_view(), name='page-list-create'),
    path('<int:shop_id>/pages/<int:pk>/', views.PageDetailView.as_view(), name='page-detail'),
]
