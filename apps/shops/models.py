from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_shops')
    name = models.CharField(max_length=255, verbose_name='Название магазина')
    domain = models.CharField(max_length=255, unique=True, verbose_name='Домен')
    description = models.TextField(blank=True, verbose_name='Описание')
    theme = models.CharField(max_length=100, default='default', verbose_name='Тема')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
    
    def __str__(self):
        return self.name

class ShopMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('editor', 'Редактор'),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='manager')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['shop', 'user']
        verbose_name = 'Участник магазина'
        verbose_name_plural = 'Участники магазина'
    
    def __str__(self):
        return f"{self.user.username} - {self.shop.name}"

class Page(models.Model):
    PAGE_TYPES = [
        ('home', 'Главная'),
        ('catalog', 'Каталог'),
        ('about', 'О нас'),
        ('contacts', 'Контакты'),
        ('custom', 'Пользовательская'),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='URL')
    content = models.JSONField(default=dict, verbose_name='Содержимое')
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, default='custom')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    seo_title = models.CharField(max_length=255, blank=True, verbose_name='SEO заголовок')
    seo_description = models.TextField(blank=True, verbose_name='SEO описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['shop', 'slug']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
    
    def __str__(self):
        return f"{self.shop.name} - {self.title}"
