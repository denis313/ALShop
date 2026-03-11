from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
import asyncio
from bot import bot
from keyboard import kb_buy
from lexicon import lexicon
from service import get_photo, create_payment, get_photo2, get_photo3

router = Router()
router.message.filter(F.chat.type == 'private')


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    loop = asyncio.get_event_loop()
    url, id_prepayment = await loop.run_in_executor(None,
                                                    create_payment,
                                                    300,
                                                    'Покупка игры',
                                                    message.from_user.id,
                                                    message.from_user.username or None)
    kb = kb_buy(id_payment=id_prepayment, url=url)


    loop = asyncio.get_event_loop()
    url, id_prepayment = await loop.run_in_executor(None,
                                                    create_payment,
                                                    100,
                                                    'Рождество',
                                                    message.from_user.id,
                                                    message.from_user.username or None)
    kb2 = kb_buy(id_payment=id_prepayment, url=url)
    await bot.send_photo(chat_id=message.from_user.id, photo=get_photo3(), caption=lexicon['about'])
    await bot.send_photo(chat_id=message.from_user.id, photo=get_photo(), caption=lexicon['start'], reply_markup=kb)
    await bot.send_photo(chat_id=message.from_user.id, photo=get_photo2(), caption=lexicon['christmas'], reply_markup=kb2)
    # await bot.send_media_group(media=[get_photo(), get_photo()])

