from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_menu = InlineKeyboardMarkup(inline_keyboard=[
   [
      InlineKeyboardButton(
         text='Тестовый старт',
         callback_data='test_msg_1'
      )
   ],
   [
      InlineKeyboardButton(
         text='Карта',
         callback_data='map'
      )
   ],
   [
      InlineKeyboardButton(
         text='Достижения',
         callback_data='achievements'
      )
   ],
])