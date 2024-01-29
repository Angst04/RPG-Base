from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

async def everton_quests(callback):
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Арнольд', callback_data='quest_arnold'))
   
   builder.row(InlineKeyboardButton(text='Назад', callback_data='everton_back'))
   
   await callback.message.edit_text(text='В ратуше вы замечаете несколько интересных персон, которые явно что-то хотят от вас', reply_markup=builder.as_markup())