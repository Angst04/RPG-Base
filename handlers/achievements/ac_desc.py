from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == 'Серьёзный выбор')
async def AC1(callback: CallbackQuery):
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Назад', callback_data='achievements'))
   await callback.message.edit_text(text='Описание достижения "Серьёзный выбор"', reply_markup=builder.as_markup())
   
@router.callback_query(F.data == 'Не менее серьёзный выбор')
async def AC1(callback: CallbackQuery):
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Назад', callback_data='achievements'))
   await callback.message.edit_text(text='Описание достижения "Не менее серьёзный выбор"', reply_markup=builder.as_markup())