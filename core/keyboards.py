from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(inline_keyboard=[
   [
      InlineKeyboardButton(
         text='В бой',
         callback_data='#'
      )
   ],
   [
      InlineKeyboardButton(
         text='Достижения',
         callback_data='achievements'
      )
   ]
])