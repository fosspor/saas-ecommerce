from django.db import models
from django.contrib.auth import get_user_model
from apps.shops.models import Shop
from apps.products.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
        ('returned', 'Возврат'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('failed', 'Ошибка оплаты'),
        ('refunded', 'Возвращен'),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Номер заказа')
    
    # Контактная информация
    customer_email = models.EmailField(verbose_name='Email клиента')
    customer_phone = models.CharField(max_length=20, verbose_name='Телефон клиента')
    customer_first_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    customer_last_name = models.CharField(max_length=100, verbose_name='Фамилия клиента')
    
    # Адрес доставки
    shipping_address_line1 = models.CharField(max_length=255, verbose_name='Адрес доставки 1')
    shipping_address_line2 = models.CharField(max_length=255, blank=True, verbose_name='Адрес доставки 2')
    shipping_city = models.CharField(max_length=100, verbose_name='Город доставки')
    shipping_state = models.CharField(max_length=100, blank=True, verbose_name='Область/регион')
    shipping_postcode = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    shipping_country = models.CharField(max_length=100, verbose_name='Страна доставки')
    
    # Адрес плательщика
    billing_address_line1 = models.CharField(max_length=255, verbose_name='Адрес плательщика 1')
    billing_address_line2 = models.CharField(max_length=255, blank=True, verbose_name='Адрес плательщика 2')
    billing_city = models.CharField(max_length=100, verbose_name='Город плательщика')
    billing_state = models.CharField(max_length=100, blank=True, verbose_name='Область/регион')
    billing_postcode = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    billing_country = models.CharField(max_length=100, verbose_name='Страна плательщика')
    
    # Финансовая информация
    currency = models.CharField(max_length=3, default='RUB', verbose_name='Валюта')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма товаров')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость доставки')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Налоги')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Скидка')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая сумма')
    
    # Статусы
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, 
                                    default='pending', verbose_name='Статус оплаты')
    
    # Дополнительно
    notes = models.TextField(blank=True, verbose_name='Примечания')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP адрес')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ #{self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    product_name = models.CharField(max_length=255, verbose_name='Название товара')
    product_sku = models.CharField(max_length=100, verbose_name='Артикул товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая цена')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ключ сессии')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        if self.user:
            return f"Корзина пользователя {self.user.username}"
        return f"Корзина сессии {self.session_key}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'product']
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзины'
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
