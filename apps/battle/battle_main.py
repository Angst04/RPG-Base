from asyncio import sleep
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from apps.battle.enemies import enemy_1, enemy_2
from apps.battle import battle_func

from random import choice

router = Router()

@router.callback_query(F.data == 'find_enemy')
async def f(callback: CallbackQuery):
   builder = InlineKeyboardBuilder()
      
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
      cbd = 'battle_everton'
   elif now_location == 'Амбербрук':
      cbd = 'battle_amberbrook'
   builder.row(InlineKeyboardButton(text='В бой!', callback_data=cbd))
   builder.row(InlineKeyboardButton(text='Отмена', callback_data='menu'))
   
   await callback.message.edit_text(text='Противник найден', reply_markup=builder.as_markup())


@router.callback_query(F.data == 'battle_everton')
async def f(callback: CallbackQuery):
   enemies = [
      'Лихорадочный',
      'Ворох'
   ]
   enemy = choice(enemies)
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Начать сражение', callback_data=f'enemy_{enemy}'))
   
   await callback.message.edit_text(text=f'Ваш противник <b>{enemy}</b>', reply_markup=builder.as_markup(), parse_mode='HTML')
   
   
router.include_routers(battle_func.router, enemy_1.router, enemy_2.router)