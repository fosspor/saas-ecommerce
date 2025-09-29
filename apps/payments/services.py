import uuid
from decimal import Decimal
from yookassa import Payment, Configuration
from django.conf import settings
from .models import Payment as PaymentModel

class YookassaService:
    def __init__(self, shop_id, secret_key):
        Configuration.account_id = shop_id
        Configuration.secret_key = secret_key
    
    def create_payment(self, amount, order_number, description, return_url, customer_email=None):
        payment = Payment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "description": description,
            "metadata": {
                "order_number": order_number
            },
            "capture": True,
            "receipt": {
                "customer": {
                    "email": customer_email
                },
                "items": []  # Будет заполнено при создании заказа
            }
        })
        
        return {
            'transaction_id': payment.id,
            'payment_url': payment.confirmation.confirmation_url,
            'status': payment.status
        }

class PaymentService:
    @staticmethod
    def create_payment_for_order(order, payment_method, return_url):
        payment = PaymentModel.objects.create(
            order=order,
            payment_method=payment_method,
            amount=order.total_amount,
            currency=order.currency
        )
        
        if payment_method.type == 'yookassa':
            service = YookassaService(
                payment_method.yookassa_shop_id,
                payment_method.yookassa_secret_key
            )
            
            result = service.create_payment(
                amount=order.total_amount,
                order_number=order.order_number,
                description=f"Оплата заказа #{order.order_number}",
                return_url=return_url,
                customer_email=order.customer_email
            )
            
            payment.transaction_id = result['transaction_id']
            payment.payment_url = result['payment_url']
            payment.status = result['status']
            payment.save()
            
            return payment
        
        # Другие методы оплаты можно добавить аналогично
        
        return payment
