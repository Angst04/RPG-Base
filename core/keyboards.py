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
         text='Отправиться в город',
         callback_data='#'
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
   ]
])

kb_map = InlineKeyboardMarkup(inline_keyboard=[
   [
      InlineKeyboardButton(
         text='Продолжить путь',
         callback_data='map'
      )
   ],
   [
      InlineKeyboardButton(
         text='Остаться',
         callback_data='menu'
      )
   ]
])