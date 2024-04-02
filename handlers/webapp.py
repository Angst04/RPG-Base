from aiogram import Router, F
from aiogram.types import Message, WebAppData
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.filters import Filter
from typing import Union, Dict, Any

import json

router = Router()

cardsID = []

with open('./data/cards.json', 'r') as file:
   card_data = json.load(file)

for card in card_data['cards']:
   cardsID.append(card['id'])

class WebAppDataFilter(Filter):
   async def __call__(self, message: Message, **kwargs) -> Union[bool, Dict[str, Any]]:
      return dict(web_app_data=message.web_app_data) if message.web_app_data else False


@router.message(WebAppDataFilter())
async def handle_web_app_data(message: Message, web_app_data: WebAppData):
   if web_app_data.data in cardsID:
      await send_card(message, web_app_data.data)
   else:
      await message.answer(web_app_data.data)


async def send_card(message, cardID):
   if cardID == 'c_0001':
      for card in card_data['cards']:
         if card['id'] == cardID:
            image = FSInputFile(card['imagePath'])
            title = card['title']

      await message.answer_photo(photo=image, caption=title)
   elif cardID == 'c_0002':
      for card in card_data['cards']:
         if card['id'] == cardID:
            image = FSInputFile(card['imagePath'])
            title = card['title']

      await message.answer_photo(photo=image, caption=title)
   else:
      await message.answer('Ошибка при выборе карты')
      print('[ERROR] Карта выбранная пользователем не найдена')