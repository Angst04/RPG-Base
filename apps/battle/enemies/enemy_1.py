# Лихорадочный
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from apps.battle.battle_func import battle_prepare

router = Router()

@router.callback_query(F.data == 'enemy_Лихорадочный')
async def f(callback: CallbackQuery):
   text = 'Жуткий волк стоит напротив вас'
   photo = FSInputFile('./data/images/cards/c_0002.png')
   amount = 14
   
   await battle_prepare(callback=callback, text=text, photo=photo, amount=amount)