from aiogram import Router, F
from aiogram.types import Message, WebAppData
#from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.filters import Filter
from typing import Union, Dict, Any

router = Router()

class WebAppDataFilter(Filter):
   async def __call__(self, message: Message, **kwargs) -> Union[bool, Dict[str, Any]]:
      return dict(web_app_data=message.web_app_data) if message.web_app_data else False


@router.message(WebAppDataFilter())
async def handle_web_app_data(message: Message, web_app_data: WebAppData):
   await message.answer(web_app_data)