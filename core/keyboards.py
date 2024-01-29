from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_menu = InlineKeyboardMarkup(inline_keyboard=[
   [
      InlineKeyboardButton(
         text='Карта',
         callback_data='map'
      )
   ],
   [
      InlineKeyboardButton(
         text='Город',
         callback_data='town'
      )
   ],
   [
      InlineKeyboardButton(
         text='Мои поручения',
         callback_data='my_quests'
      )
   ],
   [
      InlineKeyboardButton(
         text='Дополнительно',
         callback_data='menu_other'
      )
   ]
])

kb_menu_other = InlineKeyboardMarkup(inline_keyboard=[
   [
      InlineKeyboardButton(
         text='Тестовый старт',
         callback_data='test_msg_1'
      )
   ],
   [
      InlineKeyboardButton(
         text='Достижения',
         callback_data='achievements'
      )
   ],
   [
      InlineKeyboardButton(
         text='Главное меню',
         callback_data='menu'
      )
   ]
])