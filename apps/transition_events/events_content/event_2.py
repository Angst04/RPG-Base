from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import sqlite3
from time import sleep

router = Router()

async def start(callback):
   await callback.message.delete()
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Далее', callback_data='msg1'))

   await callback.message.answer(text='Что-то пошло не так...', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'msg1')
async def f(callback: CallbackQuery):
   await callback.message.edit_reply_markup()

   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Выбраться из ловушки', callback_data='menu'))

   sleep(1)
   await callback.message.answer(text='Нужно выбираться отсюда', reply_markup=builder.as_markup())