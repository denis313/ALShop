import re
import uuid
import logging
import aiohttp
from aiogram.types import Message, CallbackQuery
from requests import HTTPError
from aiogram.types import FSInputFile
from aiogram.filters import BaseFilter
from bot import bot
from config import db_config, yookassa
from yookassa import Configuration, Payment
from yookassa.domain.common import SecurityHelper
from lexicon import lexicon



def get_photo():
    photo = FSInputFile('image.jpg', filename=f'photo_img')
    return photo


def get_photo2():
    photo = FSInputFile('image2.jpg', filename=f'photo_img')
    return photo


# def create_payment(amount: int, description: str, chat_id: int, name: str):
#     account_id, secret_key = yookassa()
#     Configuration.account_id = account_id
#     Configuration.secret_key = secret_key
#     try:
#         payment = Payment.create({
#             "amount": {
#                 "value": f"{amount}.00",
#                 "currency": "RUB"
#             },
#             "confirmation": {
#                 "type": "redirect",
#                 "return_url": "https://t.me/Lael_printables_bot"
#             },
#             "payment_method_data": {
#                 "type": "sbp"
#             },
#             "capture": True,
#             "metadata": {
#                 'chat_id': chat_id
#             },
#             "receipt": {
#             "customer": {
#                 "full_name": name,
#                 "email": "email@email.ru",
#                 "phone": "79211234567"
#             },
#             "items": [
#                 {
#                     "description": "Покупка игры",
#                     "quantity": "1.00",
#                     "amount": {
#                         "value": amount,
#                         "currency": "RUB"
#                     },
#                     "vat_code": "2",
#                     "payment_mode": "full_payment",
#                     "payment_subject": "commodity",
#                     "country_of_origin_code": "CN",
#                     "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
#                     "customs_declaration_number": "10714040/140917/0090376",
#                     "excise": "20.00",
#                     "supplier": {
#                         "name": "string",
#                         "phone": "string",
#                         "inn": "string"
#                     }
#                 },
#             ]
#         },
#             "description": description
#         }, uuid.uuid4())
#         logging.debug(f"Confirmation URL: {payment.confirmation.confirmation_url}")
#         logging.debug(f"Payment ID: {payment.id}")
#         return payment.confirmation.confirmation_url, payment.id
#     except HTTPError as e:
#         # Логирование подробного ответа
#         error_response = e.response.json()
#         logging.error(f"Ошибка HTTP: {e}")
#         logging.error(f"Детали ошибки: {error_response}")
#         raise


def create_payment(amount: int, description: str, chat_id: int, name: str):
    account_id, secret_key = yookassa()
    Configuration.account_id = account_id
    Configuration.secret_key = secret_key

    try:
        payment_data = {
            "amount": {
                "value": f"{amount}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                # ОБЯЗАТЕЛЬНО добавь https://. Без него будет ошибка!
                "return_url": "https://t.me/Lael_printables_bot"
            },
            "capture": True,
            "metadata": {
                'chat_id': chat_id
            },
            "description": description,
            "receipt": {
                "customer": {
                    "full_name": name,
                    "email": "email@email.ru"  # Для теста пойдет, но лучше брать реальный
                },
                "items": [
                    {
                        "description": description,
                        "quantity": "1.00",
                        "amount": {
                            "value": f"{amount}.00",  # Здесь тоже должна быть СТРОКА
                            "currency": "RUB"
                        },
                        "vat_code": "1"  # 1 — без НДС, 2 — 0%, 3 — 10%, 4 — 20%
                    }
                ]
            }
        }

        # Мы убрали payment_method_data: sbp, чтобы ЮKassa сама предложила варианты,
        # и удалили сложные поля чека (маркировку, ГТД, поставщика).

        payment = Payment.create(payment_data, str(uuid.uuid4()))

        return payment.confirmation.confirmation_url, payment.id

    except Exception as e:
        logging.error(f"Ошибка при создании платежа: {e}")
        raise