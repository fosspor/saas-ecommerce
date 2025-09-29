import requests
from decimal import Decimal
from .models import DeliveryMethod, DeliveryZone

class CdekService:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.base_url = 'https://api.edu.cdek.ru/v2'
        self.auth_token = None
    
    def authenticate(self):
        response = requests.post(f'{self.base_url}/oauth/token', {
            'grant_type': 'client_credentials',
            'client_id': self.login,
            'client_secret': self.password
        })
        if response.status_code == 200:
            self.auth_token = response.json()['access_token']
            return True
        return False
    
    def calculate_tariff(self, from_city, to_city, weight, length=None, width=None, height=None):
        if not self.auth_token:
            if not self.authenticate():
                return None
        
        data = {
            'tariff_code': 139,  # ePacket tariff
            'from_location': {'code': from_city},
            'to_location': {'code': to_city},
            'packages': [{
                'weight': weight,
                'length': length or 20,
                'width': width or 20,
                'height': height or 20
            }]
        }
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        response = requests.post(f'{self.base_url}/calculator/tariff', json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return {
                'cost': result['delivery_sum'],
                'period_min': result['period_min'],
                'period_max': result['period_max']
            }
        return None

class DeliveryCalculator:
    @staticmethod
    def calculate_cost(delivery_method, from_city, to_city, weight, total_amount):
        # Бесплатная доставка
        if delivery_method.cost_type == 'free':
            return Decimal('0')
        
        # Фиксированная стоимость
        if delivery_method.cost_type == 'fixed':
            if delivery_method.free_threshold and total_amount >= delivery_method.free_threshold:
                return Decimal('0')
            return delivery_method.fixed_cost
        
        # Расчет для зон доставки
        zones = delivery_method.zones.filter(is_active=True)
        for zone in zones:
            # Здесь можно добавить логику проверки зон
            if zone.cost_type == 'fixed':
                return zone.fixed_cost
        
        # Расчет через API служб доставки
        if delivery_method.type == 'cdek' and delivery_method.cdek_api_login:
            service = CdekService(
                delivery_method.cdek_api_login,
                delivery_method.cdek_api_password
            )
            result = service.calculate_tariff(
                delivery_method.cdek_sender_city,
                to_city,
                weight
            )
            if result:
                return Decimal(str(result['cost']))
        
        # По умолчанию возвращаем фиксированную стоимость метода
        return delivery_method.fixed_cost
