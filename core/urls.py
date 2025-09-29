from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="E-commerce SaaS API",
      default_version='v1',
      description="API для SaaS-платформы интернет-магазинов",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/shops/', include('apps.shops.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/delivery/', include('apps.delivery.urls')),
    path('api/marketing/', include('apps.marketing.urls')),
    
    # Swagger
    path('swagger/', schema_view.with_ui(
        'swagger', 
        cache_timeout=0
    ), name='schema-swagger-ui'),
]
