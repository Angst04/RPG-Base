from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from time import sleep

from core.base_funcs import get_card

router = Router()

@router.callback_query(F.data == 'ch_0_msg_0')
async def test_msg_1(callback: CallbackQuery):
   sleep(0.3)
   await callback.message.delete_reply_markup()
   
   text = 'Довольно необычное ощущение проснуться где-то в амбаре под сеном. Обычно в такие моменты пытаешься перебрать всё произошедшее вчера, но в этот раз вы не можете вспомнить абсолютно ничего'
   
   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='Далее', callback_data='ch_0_msg_1'))
   
   await callback.message.answer(text=text, reply_markup=builder.as_markup())
   
@router.callback_query(F.data == 'ch_0_msg_1')
async def test_msg_1(callback: CallbackQuery):
   sleep(0.3)
   await callback.message.delete_reply_markup()
   
   text = 'Подумать только, в какие невероятные приключения вы могли попасть! Впрочем, может быть, вы просто решили отдохнуть от городской суеты и насладиться спокойствием сельской жизни. Всякие вещи случаются, правда?'
   
   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='Далее', callback_data='ch_0_msg_2'))
   
   await callback.message.answer(text=text, reply_markup=builder.as_markup())
   
@router.callback_query(F.data == 'ch_0_msg_2')
async def test_msg_1(callback: CallbackQuery):
   sleep(0.3)
   await callback.message.delete_reply_markup()
   
   text = 'Но сейчас у вас даже не получается вспомнить своё имя и возмножно...'
   
   await callback.message.answer(text=text)
   sleep(4)

   text = '<blockquote>Какого чёрта ты тут забыл?! Выметайся из моего курятника! - Перебил ваши рассуждения явно недоброжелательный голос</blockquote>'
   
   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='Далее', callback_data='ch_0_msg_3'))
   
   await callback.message.answer(text=text, reply_markup=builder.as_markup(), parse_mode='HTML')

@router.callback_query(F.data == 'ch_0_msg_3')
async def test_msg_1(callback: CallbackQuery):
   sleep(0.3)
   await callback.message.delete_reply_markup()
   
   text = 'Возможно до этого случая у вас была хорошая ловкость, но сейчас вы очень добротно остановили взмах какого-то бруска своей головой. Кажется это намёк на то что вы засиделись'
   
   await callback.message.answer(text=text)
   sleep(5)

   text = 'Вы оперативно вываливаетесь через ближайшее окно. Следующие 5 минут пробежки вы не очень помните, но теперь вы точно оторвались от преследователя. Отдышавшись вы понимаете, что попали в какой-то посёлок. Тут немного людей и все чем-то заняты. Вы пытаетесь остановить прохожего, но он не реагирует на вас и проходит мимо'
   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='Оглянуться', callback_data='ch_0_msg_4'))
   
   await callback.message.answer(text=text, reply_markup=builder.as_markup())
   
@router.callback_query(F.data == 'ch_0_msg_4')
async def test_msg_1(callback: CallbackQuery):
   sleep(0.3)
   await callback.message.delete_reply_markup()
   
   text = 'Перед вами разворачивается интересная картина: мужчина в рваном плаще пытается дать отпор стражнику и толпа зевак молча наблюдает за этим всем'
   
   await callback.message.answer(text=text)
   sleep(5)

   text = '<blockquote>Libertas! Не позволю кровожадным убийцам отнимать нашу пищу! - Кричит мужчина в плаще</blockquote>'
   
   await callback.message.answer(text=text, parse_mode='HTML')
   sleep(5)
   
   text = 'Бедолагу сбивают с ног и он падает в грязь. В это же мгновение стражник оголяет ножны и тянется за лезвием. Вам такой расклад не очень понравился, учитывая что все жители не особо доброжелательны к вам и униженный страдалец единственный вызывает доверие, и вы, то ли от безрассудства, то ли от желания справедливости, выхватили из рук одного из сельчан ржавый топор и набросились на стражника. Напористым тупым ударом в грудь вы опрокидываете его'
   
   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='Далее', callback_data='ch_0_msg_5'))
   
   await callback.message.answer(text=text, reply_markup=builder.as_markup())
   
   await get_card(callback=callback, card_id='c_0001')