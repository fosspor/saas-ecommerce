from django.db import models
from apps.shops.models import Shop

class Category(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='Родительская категория')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['shop', 'slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name='products')
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    short_description = models.TextField(blank=True, verbose_name='Краткое описание')
    sku = models.CharField(max_length=100, unique=True, verbose_name='Артикул')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, 
                                      null=True, blank=True, verbose_name='Старая цена')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, 
                                   null=True, blank=True, verbose_name='Себестоимость')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')
    weight = models.DecimalField(max_digits=8, decimal_places=3, 
                               null=True, blank=True, verbose_name='Вес (кг)')
    length = models.DecimalField(max_digits=8, decimal_places=3, 
                               null=True, blank=True, verbose_name='Длина (см)')
    width = models.DecimalField(max_digits=8, decimal_places=3, 
                              null=True, blank=True, verbose_name='Ширина (см)')
    height = models.DecimalField(max_digits=8, decimal_places=3, 
                               null=True, blank=True, verbose_name='Высота (см)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемый')
    meta_title = models.CharField(max_length=255, blank=True, verbose_name='Meta заголовок')
    meta_description = models.TextField(blank=True, verbose_name='Meta описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['shop', 'sku']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name='Альтернативный текст')
    is_main = models.BooleanField(default=False, verbose_name='Основное изображение')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
    
    def __str__(self):
        return f"{self.product.name} - {self.sort_order}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255, verbose_name='Название варианта')
    sku = models.CharField(max_length=100, unique=True, verbose_name='Артикул')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, 
                                      null=True, blank=True, verbose_name='Старая цена')
    stock = models.PositiveIntegerField(default=0, verbose_name='Остаток')
    weight = models.DecimalField(max_digits=8, decimal_places=3, 
                               null=True, blank=True, verbose_name='Вес (кг)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товаров'
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
