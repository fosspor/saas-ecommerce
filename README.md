# 🛍️ SaaS Платформа для Интернет-Магазинов

Полнофункциональная SaaS-платформа для создания интернет-магазинов с адаптацией под российское законодательство.

## 🚀 Возможности

### 🔐 Авторизация и пользователи
- Регистрация/авторизация (email, соцсети, Telegram)
- Роли: администратор магазина, менеджер, клиент
- Профили пользователей
- Восстановление пароля

### 🏪 Конструктор магазинов
- Drag-and-drop редактор страниц
- Темы и шаблоны (адаптивные)
- Настройка домена
- SEO-настройки

### 📦 Каталог товаров
- Модель товара с вариантами
- Импорт/экспорт CSV/Excel
- Фильтры и сортировка

### 🛒 Заказы и корзина
- Система корзины
- Оформление заказа
- Статусы заказов

### 💰 Платежные системы (РФ)
- ЮKassa, CloudPayments, Tinkoff Pay
- Поддержка НДС и ФЗ-54
- Чеки и онлайн-кассы

### 🚚 Доставка (РФ)
- Интеграция СДЭК, Почта России, Boxberry
- Расчет стоимости доставки

### 🔗 Интеграции (РФ)
- 1С: обмен товарами, заказами
- amoCRM, Bitrix24
- Wildberries, Ozon API
- Telegram-боты

### 📈 Маркетинг
- Промокоды и скидки
- Email-рассылки
- Аналитика продаж
- Отзывы и рейтинги

## 🛠 Технический стек

- **Backend**: Python (Django + Django REST Framework)
- **Frontend**: React.js + TypeScript
- **База данных**: PostgreSQL
- **Кэширование**: Redis
- **Очереди задач**: Celery
- **Контейнеризация**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## 📦 Установка

### Требования
- Docker и Docker Compose
- Git

### Запуск

```bash
# Клонирование репозитория
git clone https://github.com/ваш-логин/saas-ecommerce.git
cd saas-ecommerce

# Создание .env файла
cp .env.example .env

# Запуск Docker контейнеров
docker-compose up -d

# Применение миграций
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Сбор статических файлов
docker-compose exec web python manage.py collectstatic --noinput
