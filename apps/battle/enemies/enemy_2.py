# Ворох
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from apps.battle.battle_func import battle_prepare

router = Router()

@router.callback_query(F.data == 'enemy_Ворох')
async def f(callback: CallbackQuery):
   text = 'Враг стоит'
   photo = FSInputFile('Base/data/images/cards/c_0002.png')
   amount = 15
   
   await battle_prepare(callback=callback, text=text, photo=photo, amount=amount)