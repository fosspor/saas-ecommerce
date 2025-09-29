from django.db import models
from apps.orders.models import Order

class PaymentMethod(models.Model):
    PAYMENT_TYPES = [
        ('yookassa', 'ЮKassa'),
        ('cloudpayments', 'CloudPayments'),
        ('tinkoff', 'Tinkoff Pay'),
        ('manual', 'Ручная оплата'),
    ]
    
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, related_name='payment_methods')
    name = models.CharField(max_length=100, verbose_name='Название')
    type = models.CharField(max_length=20, choices=PAYMENT_TYPES, verbose_name='Тип')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    
    # Настройки для разных провайдеров
    yookassa_shop_id = models.CharField(max_length=100, blank=True, verbose_name='Shop ID (ЮKassa)')
    yookassa_secret_key = models.CharField(max_length=100, blank=True, verbose_name='Секретный ключ (ЮKassa)')
    
    cloudpayments_public_id = models.CharField(max_length=100, blank=True, verbose_name='Public ID (CloudPayments)')
    cloudpayments_api_secret = models.CharField(max_length=100, blank=True, verbose_name='API Secret (CloudPayments)')
    
    tinkoff_terminal_key = models.CharField(max_length=100, blank=True, verbose_name='Terminal Key (Tinkoff)')
    tinkoff_secret_key = models.CharField(max_length=100, blank=True, verbose_name='Секретный ключ (Tinkoff)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'
        ordering = ['sort_order']
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processing', 'Обрабатывается'),
        ('succeeded', 'Успешно'),
        ('failed', 'Ошибка'),
        ('cancelled', 'Отменен'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, verbose_name='Способ оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    currency = models.CharField(max_length=3, default='RUB', verbose_name='Валюта')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    
    # Данные от платежной системы
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name='ID транзакции')
    payment_url = models.URLField(blank=True, verbose_name='URL для оплаты')
    payment_data = models.JSONField(default=dict, blank=True, verbose_name='Данные оплаты')
    
    # Чеки по ФЗ-54
    receipt_url = models.URLField(blank=True, verbose_name='URL чека')
    fiscal_data = models.JSONField(default=dict, blank=True, verbose_name='Фискальные данные')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
    
    def __str__(self):
        return f"Платеж #{self.id} для заказа {self.order.order_number}"
