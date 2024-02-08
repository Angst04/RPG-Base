from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.map import map_main, map_environs
from handlers.achievements import ac_desc
from handlers.town import town_main
from handlers import my_quests

from handlers.town.town_main import cbd_town
from handlers.map.map_environs import cbd_environs
from handlers.map.map_main import cbd_map
from handlers.achievements.ac_main import cbd_achievements
from handlers.my_quests import cbd_quests

router = Router()

@router.callback_query(F.data == 'achievements')
async def f(callback: CallbackQuery):
   await cbd_achievements(callback)

@router.callback_query(F.data == 'map')
async def f(callback: CallbackQuery):
   await cbd_map(callback)
   
@router.callback_query(F.data == 'town')
async def f(callback: CallbackQuery):
   await cbd_town(callback)

@router.callback_query(F.data == 'environs')
async def f(callback: CallbackQuery):
   await cbd_environs(callback)
   
@router.callback_query(F.data == 'my_quests')
async def f(callback: CallbackQuery):
   await cbd_quests(callback)

router.include_routers(map_main.router, map_environs.router, ac_desc.router, town_main.router, my_quests.router)