from django.db import models
from apps.shops.models import Shop

class DeliveryMethod(models.Model):
    DELIVERY_TYPES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьер'),
        ('post', 'Почта'),
        ('cdek', 'СДЭК'),
        ('boxberry', 'Boxberry'),
        ('russian_post', 'Почта России'),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='delivery_methods')
    name = models.CharField(max_length=100, verbose_name='Название')
    type = models.CharField(max_length=20, choices=DELIVERY_TYPES, verbose_name='Тип')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    # Стоимость доставки
    cost_type = models.CharField(max_length=20, choices=[
        ('free', 'Бесплатно'),
        ('fixed', 'Фиксированная'),
        ('calculated', 'Рассчитывается'),
    ], default='fixed', verbose_name='Тип стоимости')
    fixed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, 
                                   verbose_name='Фиксированная стоимость')
    free_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       verbose_name='Порог бесплатной доставки')
    
    # Настройки для служб доставки
    cdek_sender_city = models.CharField(max_length=100, blank=True, verbose_name='Город отправителя (СДЭК)')
    cdek_api_login = models.CharField(max_length=100, blank=True, verbose_name='API логин (СДЭК)')
    cdek_api_password = models.CharField(max_length=100, blank=True, verbose_name='API пароль (СДЭК)')
    
    boxberry_api_token = models.CharField(max_length=100, blank=True, verbose_name='API токен (Boxberry)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'
        ordering = ['sort_order']
    
    def __str__(self):
        return self.name

class DeliveryZone(models.Model):
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=100, verbose_name='Название зоны')
    countries = models.TextField(blank=True, verbose_name='Страны (через запятую)')
    regions = models.TextField(blank=True, verbose_name='Регионы (через запятую)')
    cities = models.TextField(blank=True, verbose_name='Города (через запятую)')
    zip_codes = models.TextField(blank=True, verbose_name='Почтовые индексы (через запятую)')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    # Стоимость для зоны
    cost_type = models.CharField(max_length=20, choices=[
        ('fixed', 'Фиксированная'),
        ('calculated', 'Рассчитывается'),
    ], default='fixed', verbose_name='Тип стоимости')
    fixed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, 
                                   verbose_name='Фиксированная стоимость')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Зона доставки'
        verbose_name_plural = 'Зоны доставки'
        ordering = ['sort_order']
    
    def __str__(self):
        return f"{self.delivery_method.name} - {self.name}"

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processing', 'Обрабатывается'),
        ('shipped', 'Отправлен'),
        ('in_transit', 'В пути'),
        ('delivered', 'Доставлен'),
        ('returned', 'Возвращен'),
        ('failed', 'Ошибка'),
    ]
    
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='shipments')
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE, verbose_name='Способ доставки')
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name='Номер отслеживания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    
    # Информация о доставке
    estimated_delivery_date = models.DateField(null=True, blank=True, verbose_name='Ожидаемая дата доставки')
    actual_delivery_date = models.DateField(null=True, blank=True, verbose_name='Фактическая дата доставки')
    
    # Стоимость доставки
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость доставки')
    currency = models.CharField(max_length=3, default='RUB', verbose_name='Валюта')
    
    # Данные от службы доставки
    delivery_data = models.JSONField(default=dict, blank=True, verbose_name='Данные доставки')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Отправка'
        verbose_name_plural = 'Отправки'
    
    def __str__(self):
        return f"Отправка #{self.id} для заказа {self.order.order_number}"
