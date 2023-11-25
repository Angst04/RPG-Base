from asyncio import create_task
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import sqlite3
from .map_main import transition, cancel_event

router = Router()

@router.callback_query(F.data == 'лесопилка Доппи')
async def f(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Эвертон', 'environs', 'лесопилка Доппи'))

@router.callback_query(F.data == 'тестовая локация')
async def f(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Амбербрук', 'environs', 'тестовая локация'))