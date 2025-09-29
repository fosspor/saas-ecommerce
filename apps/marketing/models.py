from django.db import models
from apps.shops.models import Shop

class PromoCode(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Процент'),
        ('fixed_amount', 'Фиксированная сумма'),
        ('free_shipping', 'Бесплатная доставка'),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='promo_codes')
    code = models.CharField(max_length=50, unique=True, verbose_name='Код')
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, verbose_name='Тип скидки')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Значение скидки')
    
    # Ограничения
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, 
                                             null=True, blank=True, verbose_name='Минимальная сумма заказа')
    usage_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name='Лимит использования')
    usage_count = models.PositiveIntegerField(default=0, verbose_name='Количество использований')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    
    # Временные ограничения
    valid_from = models.DateTimeField(null=True, blank=True, verbose_name='Действует с')
    valid_until = models.DateTimeField(null=True, blank=True, verbose_name='Действует до')
    
    # Целевые ограничения
    applies_to_products = models.ManyToManyField('products.Product', blank=True, 
                                               verbose_name='Применяется к товарам')
    applies_to_categories = models.ManyToManyField('products.Category', blank=True,
                                                 verbose_name='Применяется к категориям')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class EmailTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('order_confirmation', 'Подтверждение заказа'),
        ('order_shipped', 'Заказ отправлен'),
        ('order_delivered', 'Заказ доставлен'),
        ('abandoned_cart', 'Брошенная корзина'),
        ('welcome', 'Приветствие'),
        ('promo', 'Промоакция'),
        ('custom', 'Пользовательский'),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='email_templates')
    name = models.CharField(max_length=255, verbose_name='Название')
    type = models.CharField(max_length=30, choices=TEMPLATE_TYPES, verbose_name='Тип')
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    content = models.TextField(verbose_name='Содержимое')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Шаблон email'
        verbose_name_plural = 'Шаблоны email'
    
    def __str__(self):
        return self.name

class EmailCampaign(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('scheduled', 'Запланирована'),
        ('sending', 'Отправляется'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='email_campaigns')
    name = models.CharField(max_length=255, verbose_name='Название')
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, verbose_name='Шаблон')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    
    # Целевая аудитория
    target_customers = models.ManyToManyField('users.User', blank=True, verbose_name='Целевые клиенты')
    target_segments = models.JSONField(default=dict, blank=True, verbose_name='Сегменты')
    
    # Расписание
    scheduled_at = models.DateTimeField(null=True, blank=True, verbose_name='Запланировано на')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Отправлено')
    
    # Статистика
    total_recipients = models.PositiveIntegerField(default=0, verbose_name='Всего получателей')
    sent_count = models.PositiveIntegerField(default=0, verbose_name='Отправлено')
    opened_count = models.PositiveIntegerField(default=0, verbose_name='Открыто')
    clicked_count = models.PositiveIntegerField(default=0, verbose_name='Переходов')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Email кампания'
        verbose_name_plural = 'Email кампании'
    
    def __str__(self):
        return self.name

class Review(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, 
                              related_name='reviews', verbose_name='Товар')
    customer = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                               related_name='reviews', verbose_name='Клиент')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, 
                            null=True, blank=True, related_name='reviews', verbose_name='Заказ')
    
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], 
                                       verbose_name='Оценка')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Отзыв')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    is_verified_purchase = models.BooleanField(default=False, verbose_name='Проверенная покупка')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'customer']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self):
        return f"{self.product.name} - {self.rating} звезд"
