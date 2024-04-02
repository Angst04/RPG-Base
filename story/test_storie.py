from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from time import sleep

from core.base_funcs import get_ac
from handlers.fragments import raise_fragment

router = Router()

@router.callback_query(F.data == 'test_msg_1')
async def test_msg_1(callback: CallbackQuery):
   await callback.message.answer(text='Добро пожаловать в тестовую историю')
   sleep(1)

   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='*Далее*', callback_data='#'))
   await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='Далее', callback_data='test_msg_2'))
   await callback.message.answer('Этап 1', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'test_msg_2')
async def test_msg_2(callback: CallbackQuery):
   await callback.message.edit_reply_markup()

   builder = InlineKeyboardBuilder()
   builder.adjust(2)
   builder.add(InlineKeyboardButton(text='Получить достижение', callback_data='test_msg_3'))
   builder.add(InlineKeyboardButton(text='Получить фрагмент', callback_data='test_msg_4'))
   await callback.message.answer(text='Куда пойдём?', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'test_msg_3')
async def test_msg_2(callback: CallbackQuery):
   await get_ac(callback=callback, ac_name='Серьёзный выбор')

   await callback.message.answer(text='Вы в саду')

@router.callback_query(F.data == 'test_msg_4')
async def test_msg_2(callback: CallbackQuery):
   await raise_fragment(callback=callback, name='Ярость бури')