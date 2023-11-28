from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

kb_menu = InlineKeyboardMarkup(inline_keyboard=[
   [
      InlineKeyboardButton(
         text='Карта',
         callback_data='map'
      )
   ],
   [
      InlineKeyboardButton(
         text='Колекция',
         web_app=WebAppInfo(url='https://angst04.github.io/RPG-Mini-Apps/')
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