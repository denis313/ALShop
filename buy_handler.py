import asyncio
import logging
import json
from datetime import timedelta, date

import yookassa
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, InputMediaPhoto, FSInputFile

from config import provider_token
from keyboard import Pay
from lexicon import lexicon


logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(Pay.filter()) #Pay.filter()
async def successful_payment_handler(callback: CallbackQuery, bot: Bot, callback_data: Pay): #, callback_data: Pay
    loop = asyncio.get_event_loop()
    payment = await loop.run_in_executor(None, yookassa.Payment.find_one, callback_data.pay_id)
    if payment.status == 'succeeded':
        if payment.description == 'Покупка игры':
            await callback.message.answer_document(document=FSInputFile('game.pdf', filename='Игра.pdf'),
                                                   caption=lexicon['succeeded'])
        elif payment.description == "Рождество":
            await callback.message.answer_document(document=FSInputFile('christmas.pdf', filename='Рождество.pdf'),
                                                   caption=lexicon['succeeded'])
    else:
        await callback.message.answer(text=lexicon['failed'])