from random import random, choice
from time import time
import sqlite3

events = [
   'Западня',
   'Чертополох',
   #'Заговор',
   #'Долгожданная встреча'
]

async def transitionEvent(callback, chance):
   conn = sqlite3.connect('Base/data/transition_events.sql', check_same_thread=False)
   last_event = conn.execute(f'SELECT last_event FROM transition_events WHERE id_tg = {callback.message.chat.id}').fetchone()[0]
   now_time = time() / 3600
   if now_time > last_event + 24:
      if random() <= chance:
         flag = False
         event = choice(events)
         conn = sqlite3.connect('Base/data/transition_events.sql', check_same_thread=False)

         if event == 'Западня':
            if conn.execute(f'SELECT Западня FROM transition_events WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 0:
               flag = True
               from apps.transition_events.events_content import event_1
               await event_1.start(callback)
            else:
               await transitionEvent(callback, chance)
         elif event == 'Чертополох':
            if conn.execute(f'SELECT Чертополох FROM transition_events WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 0:
               flag = True
               from apps.transition_events.events_content import event_2
               await event_2.start(callback)
            else:
               await transitionEvent(callback, chance)
         elif event == 'Заговор':
            # flag = True
            pass
         elif event == 'Долгожданная встреча':
            # flag = True
            pass
         else:
            pass
         if flag:
            cur = conn.cursor()

            cur.execute('UPDATE transition_events SET last_event = ? WHERE id_tg=?', (now_time, callback.message.chat.id,))
            conn.commit()
            cur.close()
         conn.close()
   else:
      print('Прошло ещё недостаточно времени') # убрать позже