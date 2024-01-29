from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from handlers.town.towns_list.everton.everton_quests import everton_quests

router = Router()

async def everton(callback):
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='☑️ Ратуша ☑️', callback_data='everton_quests'))
   builder.row(InlineKeyboardButton(text='Рынок', callback_data='#'))
   
   builder.row(InlineKeyboardButton(text='Главное меню', callback_data='menu'))
   
   await callback.message.edit_text(text='Перед вами возвышаются стены прекрасного Эвертона', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'everton_back')
async def f(callback: CallbackQuery):
   await everton(callback)
   
@router.callback_query(F.data == 'everton_quests')
async def f(callback: CallbackQuery):
   await everton_quests(callback)