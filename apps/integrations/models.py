from django.db import models
from apps.shops.models import Shop

class Integration(models.Model):
    INTEGRATION_TYPES = [
        ('wildberries', 'Wildberries'),
        ('ozon', 'Ozon'),
        ('one_c', '1С'),
        ('amocrm', 'amoCRM'),
        ('bitrix24', 'Bitrix24'),
        ('telegram_bot', 'Telegram бот'),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='integrations')
    name = models.CharField(max_length=100, verbose_name='Название')
    type = models.CharField(max_length=20, choices=INTEGRATION_TYPES, verbose_name='Тип')
    is_active = models.BooleanField(default=False, verbose_name='Активна')
    
    # Настройки подключения
    api_key = models.CharField(max_length=255, blank=True, verbose_name='API ключ')
    api_secret = models.CharField(max_length=255, blank=True, verbose_name='API секрет')
    webhook_url = models.URLField(blank=True, verbose_name='Webhook URL')
    settings = models.JSONField(default=dict, blank=True, verbose_name='Дополнительные настройки')
    
    # Статус интеграции
    last_sync = models.DateTimeField(null=True, blank=True, verbose_name='Последняя синхронизация')
    sync_status = models.CharField(max_length=20, default='idle', verbose_name='Статус синхронизации')
    error_message = models.TextField(blank=True, verbose_name='Сообщение об ошибке')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Интеграция'
        verbose_name_plural = 'Интеграции'
    
    def __str__(self):
        return f"{self.shop.name} - {self.name}"

class SyncLog(models.Model):
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name='sync_logs')
    action = models.CharField(max_length=50, verbose_name='Действие')
    status = models.CharField(max_length=20, choices=[
        ('success', 'Успешно'),
        ('error', 'Ошибка'),
        ('warning', 'Предупреждение'),
    ], verbose_name='Статус')
    message = models.TextField(verbose_name='Сообщение')
    data = models.JSONField(default=dict, blank=True, verbose_name='Данные')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Лог синхронизации'
        verbose_name_plural = 'Логи синхронизации'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.integration.name} - {self.action} - {self.created_at}"
