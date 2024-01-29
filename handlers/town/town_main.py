from aiogram import Router
from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from handlers.town.towns_list.everton import everton_main

from handlers.town.towns_list.everton.everton_main import everton

router = Router()

async def cbd_town(callback):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT now_location FROM users_map WHERE id_tg = %s', [callback.message.chat.id])
   now_location = cur.fetchone()[0]
   cur.close()
   conn.close()
   
   if now_location == 'Эвертон':
      await everton(callback)
      
router.include_routers(everton_main.router)