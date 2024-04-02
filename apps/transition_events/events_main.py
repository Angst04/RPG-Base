from random import random, choice
from time import time

import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

events = [
   'Западня',
   'Чертополох',
   #'Заговор',
   #'Долгожданная встреча'
]

async def transitionEvent(callback, chance):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   cur.execute(f'SELECT last_event FROM transition_events WHERE id_tg = %s', [callback.message.chat.id])
   last_event = cur.fetchone()[0]
   conn.close()
   cur.close()
   now_time = time() / 3600
   if now_time > last_event + 24:
      if random() <= chance:
         flag = False
         event = choice(events)
         conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
         cur = conn.cursor()

         if event == 'Западня':
            cur.execute(f'SELECT Западня FROM transition_events WHERE id_tg = %s', [callback.message.chat.id])
            if cur.fetchone()[0] == 0:
               flag = True
               from apps.transition_events.events_content import event_1
               await event_1.start(callback)
            else:
               await transitionEvent(callback, chance)
         elif event == 'Чертополох':
            cur.execute(f'SELECT Чертополох FROM transition_events WHERE id_tg = %s', [callback.message.chat.id])
            if cur.fetchone()[0] == 0:
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

            cur.execute(f'UPDATE transition_events SET last_event = %s WHERE id_tg= %s', [now_time, callback.message.chat.id])
            conn.commit()
            cur.close()
         conn.close()
   else:
      print('Прошло ещё недостаточно времени') # убрать позже