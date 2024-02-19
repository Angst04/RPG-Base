from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == 'info_hp')
async def f(callback: CallbackQuery):
   await callback.answer('Это количество оставшегося здоровья')