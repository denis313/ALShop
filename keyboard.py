from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Pay(CallbackData, prefix='pay', sep=':'):
    pay_id: str


def kb_buy(url:str, id_payment):
    kb = InlineKeyboardBuilder()
    kb.row(*[InlineKeyboardButton(text='Оплата 💳', url=url),
             InlineKeyboardButton(text='Проверка оплаты ✅',
                                  callback_data=Pay(pay_id=id_payment).pack())], #Pay(pay_id=id_payment).pack()
           width=1)
    return kb.as_markup()
